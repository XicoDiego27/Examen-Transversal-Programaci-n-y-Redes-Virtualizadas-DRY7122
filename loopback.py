from ncclient import manager
import xml.dom.minidom

# Conexión NETCONF al CSR1000v
m = manager.connect(
    host="192.168.56.104",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
    )

# Demostrar la conexion NETCONF mostrando las capacidades soportadas (modelos YANG)
print("#Capacidades soportadas (modelos YANG):")
for capability in m.server_capabilities:
    print(capability)

# Cambiar el nombre del router usando los apellidos del grupo
netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <hostname>Navarrete-Gajardo</hostname>
  </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_hostname)
print("\n#Resultado del cambio de hostname:")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Crear la interfaz Loopback 11 con IPv4 11.11.11.11/32
netconf_loopback11 = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>11</name>
    <description>Loopback creada via NETCONF - Examen DRY7122</description>
    <ip>
     <address>
      <primary>
       <address>11.11.11.11</address>
       <mask>255.255.255.255</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_loopback11)
print("\n#Resultado de la creacion de Loopback 11:")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())