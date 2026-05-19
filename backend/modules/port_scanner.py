import nmap

def scan_ports(target):
    nm = nmap.PortScanner(nmap_search_path=("C:\\Program Files (x86)\\Nmap\\nmap.exe",))

    nm.scan(target, arguments='-Pn -sT')

    results = []

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()

            for port in ports:
                state = nm[host][proto][port]['state']

                if state == 'open':
                    service = nm[host][proto][port]['name']
                    results.append({
                        "port": port,
                        "service": service
                    })

    return results