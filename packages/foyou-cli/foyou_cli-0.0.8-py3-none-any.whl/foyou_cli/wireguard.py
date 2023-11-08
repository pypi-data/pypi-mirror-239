import os
import subprocess


def adjust_wireguard_metric(gateway='10.0.0.1', metric=30):
    """自动调整 wireguard 的 metric 值，以达到分流的目的

    :param gateway: 网关地址，默认 10.0.0.1
    :param metric: 默认 30
    :return:
    """
    if not (os.name == 'nt'):
        print('仅支持 Windows')
        return
    p = subprocess.run('netsh interface ipv4 show interface'.split(), capture_output=True)
    for i in p.stdout.split(b'\r\n'):
        print(i.decode('gb18030'))
        j = i.split()
        if len(j) > 1 and j[1] == b'5':
            idx = j[0].decode()
            print('获取到 WireGuard 网卡索引', idx)
            subprocess.run(f'netsh interface ipv4 set interface {idx} metric={metric}'.split())
            subprocess.run(f'route add 0.0.0.0 mask 128.0.0.0 {gateway}'.split())
            subprocess.run('ipconfig /flushdns'.split())
            return
