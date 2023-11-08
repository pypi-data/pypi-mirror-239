#!/usr/bin/python3

# Copyright (C) 2023 Jonathan Farley
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from pathlib import Path
import argparse
import logging
import pandas as pd
from libnmap.parser import NmapParser
import importlib.metadata 

def parse_args(): # Create the arguments
	__version__ = importlib.metadata.version('superparsenmap')
	parser = argparse.ArgumentParser(description="Parses Nmap XML output to CSV or Excel format.")
	parser.add_argument("-i", "--input", help="Path to the nmap xml file.", required=True)
	parser.add_argument("-o", "--output", help="Output filename without an extension.", required=False, default=None)
	parser.add_argument("-v", "--verbose", action="count", help="Set the terminal output verbosity level.", required=False, default=0)
	parser.add_argument("-f", "--force", action="store_true", help="Overwrite the output file if it already exists.", required=False, default=False)
	parser.add_argument("-e", "--excel", action="store_true", help="Output an Excel .xlsx file.", required=False, default=False)
	parser.add_argument("-c", "--csv", action="store_true", help="Output a simple .CSV file of IP addresses and ports with service banners.", required=False, default=False)
	parser.add_argument("-t", "--txt", action="store_true", help="Output a directory of text files grouped by ports.", required=False, default=False)
	parser.add_argument("-a", "--all", action="store_true", help="Output all formats: Excel, CSV, and Text Files.", required=False, default=False)
	parser.add_argument("--version", action="version", version="SuperParseNmap {version}".format(version=__version__))
	return parser.parse_args()

def parse_nmap_xml(xml_file, verbosity):
	# Parse the Nmap XML file
	nmap_data = NmapParser.parse_fromfile(xml_file)
	
	# Initialize lists to store IP addresses and ports
	ip_addresses = []
	hostnames = []
	ports = []
	protocols = []
	services = []
	banners = []

	for host in nmap_data.hosts:
		ip = host.ipv4

		if host.is_up(): # Check if host is up
			
			hostname = 'N/A' # Default value for hosts without hostnames
			if host.hostnames: # Get hostnames
				hostname = host.hostnames[0]
			# print ('[*] {0} - {1}'.format(ip, hostname))

		for service in host.services:
			if service.open(): # Check if port is open
				ip_addresses.append(ip)
				ports.append(service.port)
				hostnames.append(hostname)
				protocols.append(service.protocol)
				services.append(service.service)
				banners.append(service.banner)

				if verbosity:
					print ('[*] {0} - {1} - {2} - {3} - {4}'.format(ip_addresses[-1], ports[-1], hostnames[-1], protocols[-1], services[-1], banners[-1]))
	if verbosity:
		print()

	df = pd.DataFrame(list(zip(ip_addresses, ports, hostnames, protocols, services, banners)), columns=['IP','Port', "Hostnames", 'Protocol', 'Service', 'Banner'])
	return df
			
	# Create a Pandas DataFrame
	data = {'IP Address': "127.0.0.1"}
	# data = {'IP Address': ip_addresses, 'Port': ports}
	df = pd.DataFrame(data)
	
	return df

def export_excel(df, output_file): #  Save DataFrame to Excel format
	writer = pd.ExcelWriter(output_file, engine='xlsxwriter') # Create a nwe writer object for xlsx documents
	df.to_excel(writer, sheet_name='All', index=False, header=True) # Save the dataframe of all hosts as a sheet

	# Group unique ports into different Excel sheets
	grouped = df.groupby("Port")

	for port, data in grouped:
		sheet_name = f'{port}'
		data.to_excel(writer, sheet_name=sheet_name, index=False)

	writer.close()
	print(f"Host data saved to: {output_file}")

def export_csv(df, output_file): # Save DataFrame to CSV
	df.to_csv(output_file, index=False)
	print(f"Host data saved to: {output_file}")

def export_txt_by_port(df, output_file):
	output_file.mkdir(parents=False, exist_ok=True)

	port_dict = gen_port_dict()
	# Group unique ports into different sheets
	grouped = df.groupby("Port")


	for port, data in grouped:
		port_name = port_dict.get(port)
		if port_name:
			port_name = "_"+port_name
		else:
			port_name = ""

		ip_addresses = data["IP"]
		file_name = f'{port}{port_name}.txt'
		file_path = Path(output_file) / file_name
	
		with open(file_path, 'w') as file:
			file.write('\n'.join(ip_addresses))

	print(f"Port text files generated to: {output_file}")

def main():
   
	args = parse_args()

	verbosity = False
	if args.verbose > 0 :
		verbosity = True

	if args.all:
		args.excel = args.csv = args.txt = True

	nmap_xml_file = Path(args.input)
	output_file = args.output
	
	if not nmap_xml_file.is_file():
		print(f"Error: The file '{nmap_xml_file}' does not exist.")
		return
	
	if output_file is None:
		output_file = Path(Path.cwd() / "hosts")
	if output_file:
		output_file = Path(output_file)
		output_file_wo_ext = output_file.with_suffix('') # Strip off extension

	# Parse Nmap XML and create a DataFrame
	df = parse_nmap_xml(nmap_xml_file, verbosity)
	
	if (args.excel):
		output_file_xlsx_ext = output_file_wo_ext.with_suffix('.xlsx')
		if ( not output_file_xlsx_ext.exists() or args.force): 
			export_excel(df, output_file_xlsx_ext)
		else:
			print("[!!] ERROR: File", output_file_xlsx_ext ,"Exists. Skipping. Overwrite with the parameter '--force'")

	if args.csv:
		output_file_csv_ext = output_file_wo_ext.with_suffix('.csv')
		if ( not output_file_csv_ext.exists() or args.force): 
			export_csv(df, output_file_csv_ext)
		else:
			print("[!!] ERROR: File", output_file_xlsx_ext ,"Exists. Skipping. Overwrite with the parameter '--force'")

	if args.txt:
		if ( not output_file_wo_ext.exists() or args.force): 
			export_txt_by_port(df, output_file_wo_ext)
		else:
			print("[!!] ERROR: Directory", output_file_xlsx_ext ,"Exists. Skipping. Overwrite with the parameter '--force'")
	print()

def gen_port_dict():
	port_dict = {
		80: "http",
		23: "telnet",
		443: "https",
		21: "ftp",
		22: "ssh",
		25: "smtp",
		3389: "ms-wbt-server",
		110: "pop3",
		445: "smb-microsoft-ds",
		139: "netbios-ssn",
		143: "imap",
		53: "dns",
		135: "msrpc",
		3306: "mysql",
		8080: "http-proxy",
		1723: "pptp",
		111: "rpcbind",
		995: "pop3s",
		993: "imaps",
		5900: "vnc",
		1025: "NFS-or-IIS",
		587: "submission",
		8888: "sun-answerbook",
		199: "smux",
		1720: "h323q931",
		465: "smtps",
		548: "afp",
		113: "ident",
		81: "hosts2-ns",
		6001: "X11:1",
		10000: "snet-sensor-mgmt",
		514: "shell",
		5060: "sip",
		179: "bgp",
		1026: "LSA-or-nterm",
		2000: "cisco-sccp",
		8443: "https-alt",
		8000: "http-alt",
		32768: "filenet-tms",
		554: "rtsp",
		26: "rsftp",
		1433: "ms-sql-s",
		2001: "dc",
		515: "printer",
		8008: "http",
		1027: "IIS",
		5666: "nrpe",
		646: "ldp",
		5000: "upnp",
		5631: "pcanywheredata",
		631: "ipp",
		8081: "blackice-icecap",
		2049: "nfs",
		88: "kerberos-sec",
		79: "finger",
		5800: "vnc-http",
		106: "pop3pw",
		2121: "ccproxy-ftp",
		1110: "nfsd-status",
		6000: "X11",
		513: "login",
		990: "ftps",
		5357: "wsdapi",
		427: "svrloc",
		543: "klogin",
		544: "kshell",
		5101: "admdog",
		144: "news",
		7: "echo",
		389: "ldap",
		8009: "ajp13",
		3128: "squid-http",
		444: "snpp",
		9999: "abyss",
		5009: "airport-admin",
		7070: "realserver",
		5190: "aol",
		3000: "ppp",
		5432: "postgresql",
		1900: "upnp",
		3986: "mapper-ws_ethd",
		13: "daytime",
		1029: "ms-lsa",
		9: "discard",
		5051: "ida-agent",
		873: "rsync",
		1755: "wms",
		2717: "pn-requester",
		4899: "radmin",
		9100: "jetdirect",
		119: "nntp",
		37: "time",
	}
	return port_dict

if __name__ == "__main__":
	main()
