vlan = int(input("Ingrese el número de VLAN: "))

if vlan >= 1 and vlan <= 50:
    print("La VLAN pertenece al rango normal.")
elif vlan >= 51 and vlan <= 100:
    print("La VLAN pertenece al rango extendido.")
else:
    print("Número de VLAN inválido.")