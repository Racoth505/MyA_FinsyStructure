import boto3
from datetime import datetime, timedelta

# Configuración de clientes
ec2 = boto3.client('ec2', region_name='us-east-1')
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
s3 = boto3.client('s3')

def obtener_reporte():
    print(f"=== REPORTE DE RECURSOS FINSY - {datetime.now()} ===")
    
    # 1. Listar instancias EC2 y su estado
    print("\n--- Estado de Instancias EC2 ---")
    instances = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['Finsy-*']}])
    for res in instances['Reservations']:
        for inst in res['Instances']:
            name = next((t['Value'] for t in inst['Tags'] if t['Key'] == 'Name'), 'Sin Nombre')
            instance_id = inst['InstanceId']
            estado = inst['State']['Name']
            print(f"Instancia: {name} | ID: {instance_id} | Estado: {estado}")

            # 2. Obtener métricas de CPU de CloudWatch para cada instancia
            if estado == 'running':
                stats = cloudwatch.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                    StartTime=datetime.utcnow() - timedelta(minutes=10),
                    EndTime=datetime.utcnow(),
                    Period=300,
                    Statistics=['Average']
                )
                if stats['Datapoints']:
                    cpu = stats['Datapoints'][0]['Average']
                    print(f"   > Uso de CPU (últimos 5 min): {cpu:.2f}%")

    # 3. Listar buckets en S3
    print("\n--- Buckets y Objetos en S3 ---")
    buckets = s3.list_buckets()
    for b in buckets['Buckets']:
        if 'finsy' in b['Name']:
            print(f"Bucket: {b['Name']}")
            objs = s3.list_objects_v2(Bucket=b['Name'])
            if 'Contents' in objs:
                for obj in objs['Contents']:
                    print(f"   - {obj['Key']} ({obj['Size']} bytes)")

if __name__ == "__main__":
    obtener_reporte()