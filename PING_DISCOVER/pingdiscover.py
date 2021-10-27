#!/usr/bin/python

# Author: @Praveen Pasunuri
# Usage: python pingdiscover.py --subnet "192.168.0.0/24" --concurrent 8 --timeout 2

from argparse import ArgumentParser
from aioping import verbose_ping, ping

import asyncio
import ipaddress
import logging
import socket

class PingScanner():
    def __init__(self):
        # Logging Enabled
        logging.basicConfig(filename="ping_discover.log",level=logging.INFO,format='%(name)s - %(levelname)s - %(message)s',force=True)
        # Default Semaphore
        self.semaphore = asyncio.Semaphore(20)
    
    def set_semaphore(self, concurrency_level):
        """Semaphore sets no of concurrent processes"""
        self.semaphore = asyncio.Semaphore(int(concurrency_level))

    async def _do_ping(self, host, timeout=5):
        """do_ping pings the network , default timeout for 5sec"""
        try:
            # Semaphore for concurrent processes 
            async with self.semaphore:
                # socket.AddressFamily.AF_INET - Denotes IPV4 addresses only, and will ignore IPV6 addresses
                delay = await verbose_ping(host, family=socket.AddressFamily.AF_INET,  timeout=timeout) * 1000
                logging.debug(f"{host} ping response in {delay:0.4f}ms")
                return delay
        except TimeoutError:
            logging.error("%s timed out" % host)
        except Exception as e:
                pass

    def ping_discover(self, subnet="192.168.0.0/24", timeout="5"):
        try:
            timeout = int(timeout)
        except Exception:
            logging.error("Invalid Timeout or Concurrent Level")
            return False
        
        try:
            network = ipaddress.IPv4Network(subnet) #-- Only for IPV4network
            #network = ipaddress.ip_network(subnet, strict=False) #1.1 #-- Work for IPV6 and IPV4 too
        except ValueError:
            logging.error('address/netmask is invalid for IPv4:', subnet)
            return False
        
        loop = asyncio.get_event_loop()
        tasks = self.create_tasks(network,timeout)
        loop.run_until_complete(self.create_tasks(network,timeout))
        loop.close()
        
    async def create_tasks(self,network,timeout):
        tasks = []
        for index, ip in enumerate(network.hosts()):
            tasks.append(asyncio.ensure_future(self._do_ping(f"{ip}",  timeout=timeout)))
        await asyncio.wait(tasks)
        

    def main(self):
        parser = ArgumentParser()
        parser.add_argument("-s", "--subnet", dest="subnet", required=True,
                            help="Subnet + Netmask  eg. 192.168.0.0/24")
        parser.add_argument("-c", "--concurrent", dest="concurrency_level",
                            help="Concurrency Level, Number of concurrent hosts that are pinged at the same time")
        parser.add_argument("-t", "--timeout", dest="timeout", default="5",
                            help="The number of seconds after giving up on pinging a host")
        self.args = parser.parse_args()


if __name__ == '__main__':
    # python3 pingdiscover.py -s "192.168.0.0/24" --concurrent 8 --timeout 2
    # ping('google.com', timeout=3000, count=3, delay=0.5, verbose=True)
    logging.info("Started ping scanning")
    pingScanner = PingScanner()
    pingScanner.main()
    pingScanner.set_semaphore(pingScanner.args.concurrency_level)
    logging.debug("Arguments", pingScanner.args)
    pingScanner.ping_discover(subnet=pingScanner.args.subnet, timeout=pingScanner.args.timeout)
    logging.info("Ping scanning completed")
