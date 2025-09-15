from ncclient import manager
import xml.dom.minidom

device = {
    "host": "sbx-nxos-mgmt.cisco.com",
    "port": 830,
    "username": "admin",
    "password": "",  # replace with correct password
    "hostkey_verify": False
}

# NX-OS native filter for interface *operational state*
filter_xml = """
<filter>
  <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <intf-items>
    </intf-items>
  </System>
</filter>
"""

def main():
    with manager.connect(**device) as m:
        # Use get() for operational state (not get_config)
        response = m.get(filter=filter_xml)
        # Pretty print XML
        xml_dom = xml.dom.minidom.parseString(response.xml)
        pretty_xml = xml_dom.toprettyxml(indent="  ")
        print("===== NETCONF OPERATIONAL STATE =====")
        print(pretty_xml)

if __name__ == "__main__":
    main()
