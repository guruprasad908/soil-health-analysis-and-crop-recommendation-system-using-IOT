import socket
import time

def test_port_connectivity(host, port, timeout=5):
    """Test if a port is open and accepting connections"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} on {host} is open and accepting connections")
            return True
        else:
            print(f"❌ Port {port} on {host} is closed or not accepting connections")
            return False
    except Exception as e:
        print(f"❌ Error testing connectivity to {host}:{port} - {e}")
        return False

def test_network_interfaces():
    """Get all network interfaces and their IP addresses"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"Local IP: {local_ip}")
        
        # Get all IP addresses
        import netifaces
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    print(f"Interface {interface}: {addr_info['addr']}")
    except Exception as e:
        print(f"Error getting network interfaces: {e}")

if __name__ == "__main__":
    print("Testing network connectivity for Arduino IoT connection...")
    print("=" * 50)
    
    # Test the specific IP and port the Arduino is trying to connect to
    test_port_connectivity("localhost", 8000)
    
    # Test localhost as well
    test_port_connectivity("127.0.0.1", 8000)
    
    print("\nNetwork Interface Information:")
    print("=" * 50)
    test_network_interfaces()