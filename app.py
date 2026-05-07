import boto3

# Configuración centralizada
# NOTA: Asegúrate de que este ID de Security Group exista en tu consola actual
SG_ID = 'sg-0147f028d35b6daa0'
AMI_UBUNTU = 'ami-0e2c8ccd4e1223c32' # Ubuntu 24.04 LTS en us-east-1
LLAVE_NOMBRE = 'MyA_Key' # Nombre de tu llave en AWS

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
s3 = boto3.client('s3')

def crear_ec2():
    while True:
        entrada = input("\n¿Cuántas instancias deseas crear? (0 para regresar, max 9): ")
        if not entrada.isdigit(): continue
        cantidad = int(entrada)
        if cantidad == 0: return
        if 1 <= cantidad <= 9: break
        print("Error: Rango de 1 a 9.")

    print(f"Iniciando creación de {cantidad} instancia(s)...")

    for i in range(cantidad):
        nombre = input(f"Nombre para la instancia {i+1}: ")

        instance = ec2.create_instances(
            ImageId=AMI_UBUNTU, 
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName=LLAVE_NOMBRE,
            SecurityGroupIds=[SG_ID],
            # CRÍTICO: LabRole es el único permitido en Learner Lab
            IamInstanceProfile={'Name': 'LabInstanceProfile'}, 
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': nombre}]
            }],
            BlockDeviceMappings=[{
                'DeviceName': '/dev/sda1',
                'Ebs': {'VolumeSize': 8, 'VolumeType': 'gp3'}
            }]
        )
        print(f"✅ Creada: {nombre} | ID: {instance[0].id}")

def reporte_recursos():
    print("\n--- Reporte de Instancias ---")
    instances = client.describe_instances()
    total = 0
    for res in instances['Reservations']:
        for ins in res['Instances']:
            total += 1
            print(f"ID: {ins['InstanceId']} | Tipo: {ins['InstanceType']} | Estado: {ins['State']['Name']}")
    print(f"Total: {total}/9 instancias ocupadas.")

def listar_s3():
    print("\n--- Listando Buckets S3 ---")
    buckets = s3.list_buckets()
    for b in buckets['Buckets']:
        print(f"\nBucket: {b['Name']}")
        try:
            objs = s3.list_objects_v2(Bucket=b['Name'])
            if 'Contents' in objs:
                for obj in objs['Contents']:
                    print(f"  - {obj['Key']} ({obj['Size']} bytes)")
            else:
                print("  (Bucket vacío)")
        except Exception as e:
            print(f"  (Error de acceso: {e})")

def menu():
    while True:
        print("\n===== GESTIÓN DE INFRAESTRUCTURA (FINSY) =====")
        print("1. Desplegar EC2 (Ubuntu)")
        print("2. Reporte de recursos")
        print("3. Listar S3")
        print("4. Salir")
        op = input("Selección: ")
        if op == "1": crear_ec2()
        elif op == "2": reporte_recursos()
        elif op == "3": listar_s3()
        elif op == "4": break

if __name__ == "__main__":
    menu()