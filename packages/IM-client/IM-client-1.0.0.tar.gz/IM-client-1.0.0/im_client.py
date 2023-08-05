#! /usr/bin/env python
#
# IM - Infrastructure Manager
# Copyright (C) 2011 - GRyCAP - Universitat Politecnica de Valencia
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

import xmlrpclib
import sys
import os
from optparse import OptionParser, Option, IndentedHelpFormatter
import ConfigParser
from radl import radl_parse
from radl.radl import RADL

__version__ = "1.0.0"

class PosOptionParser(OptionParser):
	def format_help(self, formatter=None):
		class Positional(object):
			def __init__(self, args):
				self.option_groups = []
				self.option_list = args

		positional = Positional(self.positional)
		formatter = IndentedHelpFormatter()
		formatter.store_option_strings(positional)
		output = ['\n', formatter.format_heading("Operation")]
		formatter.indent()
		pos_help = [formatter.format_option(opt) for opt in self.positional]
		pos_help = [line.replace('--','') for line in pos_help]
		output += pos_help
		return OptionParser.format_help(self, formatter) + ''.join(output)

	def add_operation_help(self, arg, helpstr):
		try:
			args = self.positional
		except AttributeError:
			args = []
		args.append(Option('--' + arg, action='store_true', help=helpstr))
		self.positional = args

	def set_out(self, out):
		self.out = out

# From IM.auth
def read_auth_data(filename):
	if isinstance(filename, list):
		lines = filename
	else:
		auth_file = open(filename, 'r')
		lines = auth_file.readlines()
		auth_file.close()

	res = []
	i = 0
	for line in lines:
		line = line.strip()
		if len(line) > 0 and not line.startswith("#"):
			auth = {}
			tokens = line.split(";")
			for token in tokens:
				key_value = token.split(" = ")
				if len(key_value) != 2:
					break;
				else:
					auth[key_value[0].strip()] = key_value[1].strip().replace("\\n","\n")
			res.append(auth)
	
	return res

def get_inf_id(args):
	if len(args) >= 1:
		if args[0].isdigit():
			inf_id = int(args[0])
			return inf_id
		else:
			print "Incorrect Inf ID"
			sys.exit(1)
	else:
		print "Inf ID not specified"
		sys.exit(1)

if __name__ == "__main__":
	config = ConfigParser.RawConfigParser()
	config.read(['im_client.cfg', os.path.expanduser('~/.im_client.cfg')])

	default_auth_file = None
	default_xmlrpc = "http://localhost:8888"
	XMLRCP_SSL = False
	XMLRCP_SSL_CA_CERTS = "./pki/ca-chain.pem"

	if config.has_option('im_client', "auth_file"):
		default_auth_file = config.get('im_client', "auth_file")
	if config.has_option('im_client', "xmlrpc_url"):
		default_xmlrpc = config.get('im_client', "xmlrpc_url")
	if config.has_option('im_client', "xmlrpc_ssl"):
		XMLRCP_SSL = config.getboolean('im_client', "xmlrpc_ssl")
	if config.has_option('im_client', "xmlrpc_ssl_ca_certs"):
		XMLRCP_SSL_CA_CERTS = config.get('im_client', "xmlrpc_ssl_ca_certs")

	NOTICE="\n\n\
IM - Infrastructure Manager\n\
Copyright (C) 2011 - GRyCAP - Universitat Politecnica de Valencia\n\
This program comes with ABSOLUTELY NO WARRANTY; for details please\n\
read the terms at http://www.gnu.org/licenses/gpl-3.0.txt.\n\
This is free software, and you are welcome to redistribute it\n\
under certain conditions; please read the license at \n\
http://www.gnu.org/licenses/gpl-3.0.txt for details."

	parser = PosOptionParser(usage="%prog [-u|--xmlrpc-url <url>] [-a|--auth_file <filename>] operation op_parameters"+NOTICE, version="%prog " + __version__)
	parser.add_option("-a", "--auth_file", dest="auth_file", nargs=1, default=default_auth_file, help="Fichero con los datos de autenticacion", type="string")
	parser.add_option("-u", "--xmlrpc-url", dest="xmlrpc", nargs=1, default=default_xmlrpc, help="Direccion url xmlrpc del demonio InfrastructureManager", type="string")
	parser.add_operation_help('list', '')
	parser.add_operation_help('create','<radl_file>')
	parser.add_operation_help('destroy','<inf_id>')
	parser.add_operation_help('getinfo','<inf_id> [status|radl|cloud|radl_attribute]')
	parser.add_operation_help('getcontmsg','<inf_id>')
	parser.add_operation_help('getvminfo','<inf_id> <vm_id>')
	parser.add_operation_help('addresource','<inf_id> <radl_file>')
	parser.add_operation_help('removeresource', '<inf_id> <vm_id>')
	parser.add_operation_help('alter','<inf_id> <vm_id> <radl_file>')
	parser.add_operation_help('start','<inf_id>')
	parser.add_operation_help('stop','<inf_id>')
	parser.add_operation_help('reconfigure','<inf_id> [<radl_file>]')

	(options, args) = parser.parse_args()

	if options.auth_file is None:
		parser.error("Auth file not specified")

	auth_data = read_auth_data(options.auth_file)
	
	if auth_data is None:
		parser.error("Auth file with incorrect format.")

	if len(args) < 1:
		parser.error("operation not specified. Use --help to show all the available operations.")
	operation = args[0].lower()
	args = args[1:]

	if (operation not in ["removeresource", "addresource", "create", "destroy", "getinfo", "list", "stop", "start", "alter", "getcontmsg", "getvminfo", "reconfigure"]):
		parser.error("operation not recognised.  Use --help to show all the available operations")

	if XMLRCP_SSL:
		print "Secure connection with: " + options.xmlrpc
		from springpython.remoting.xmlrpc import SSLClient
		server = SSLClient(options.xmlrpc, XMLRCP_SSL_CA_CERTS)
	else:
		print "Connected with: " + options.xmlrpc
		server = xmlrpclib.ServerProxy(options.xmlrpc,allow_none=True)

	if operation == "removeresource":
		inf_id = get_inf_id(args)
		if len(args) >= 2:
			vm_list = args[1]
		else:
			print "Coma separated VM list to remove not specified"
			sys.exit(1)
		
		(success, vms_id) = server.RemoveResource(inf_id, vm_list, auth_data)
	
		if success:
			print str(vms_id) + " resources deleted: "
		else:
			print "ERROR deleting resources from the infrastructure: " + vms_id
			sys.exit(1)
	
	elif operation == "addresource":
		inf_id = get_inf_id(args)
		if len(args) >= 2:
			if not os.path.isfile(args[1]):
				print "RADL file '" + args[1] + "' not exist"
				sys.exit(1)
		else:
			print "RADL file to add resources not specified"
			sys.exit(1)

		radl = radl_parse.parse_radl(args[1])
		
		(success, vms_id) = server.AddResource(inf_id, str(radl), auth_data)
			
		if success:
			print "Resources added: " + str(vms_id)
		else:
			print "ERROR adding resources to infrastructure: " + vms_id
			sys.exit(1)
	
	elif operation == "create":
		if len(args) >= 1:
			if not os.path.isfile(args[0]):
				print "RADL file '" + args[0] + "' not exist"
				sys.exit(1)
		else:
			print "RADL file to create inf. not specified"
			sys.exit(1)

		radl = radl_parse.parse_radl(args[0])
	
		(success, inf_id) = server.CreateInfrastructure(str(radl), auth_data)
	
		if success:
			print "Infrastructure created: " + str(inf_id)
		else:
			print "ERROR creating the infrastructure: " + inf_id
			sys.exit(1)
			
	elif operation == "alter":
		inf_id = get_inf_id(args)
		if len(args) >= 2:
			vm_id = args[1]
		else:
			print "VM ID to Modify not specified"
			sys.exit(1)
		if len(args) >= 3:
			if not os.path.isfile(args[2]):
				print "RADL file '" + args[2] + "' not exist"
				sys.exit(1)
		else:
			print "RADL file to modify the VM not specified"
			sys.exit(1)

		radl = radl_parse.parse_radl(args[2])
	
		(success, res) = server.AlterVM(inf_id, vm_id, str(radl), auth_data)
	
		if success:
			print "VM modified: " + str(res)
		else:
			print "ERROR modifying the VM: " + res
			sys.exit(1)
			
	elif operation == "reconfigure":
		inf_id = get_inf_id(args)
		radl = ""
		if len(args) >= 2:
			if not os.path.isfile(args[1]):
				print "RADL file '" + args[1] + "' not exist"
				sys.exit(1)
			else:
				radl = radl_parse.parse_radl(args[0])
	
		(success, res) = server.Reconfigure(inf_id, str(radl), auth_data)
	
		if success:
			print "Infrastructure reconfigured: " + str(res)
		else:
			print "ERROR reconfiguring the infrastructure: " + res
			sys.exit(1)
	
	elif operation == "getcontmsg":
		inf_id = get_inf_id(args)

		(success, res) = server.GetInfrastructureInfo(inf_id, auth_data)
		if success:
			cont_out = res['cont_out']
			
			if len(cont_out) > 0:
				print "Msg Contextualizator: \n"
				print cont_out
			else:
				print "No Msg Contextualizator avaliable\n"
		else:
			print res

	elif operation == "getvminfo":
		inf_id = get_inf_id(args)
		if len(args) >= 2:
			vm_id = args[1]
		else:
			print "VM ID to get info not specified"
			sys.exit(1)

		propiedad = None
		if len(args) >= 2:
			propiedad = args[2]

		(success, info)  = server.GetVMInfo(inf_id, vm_id, auth_data)

		if success:
			if propiedad:
				info_radl = radl_parse.parse_radl(info['info'])
				for system in info_radl.systems:
					prop = system.getValue(propiedad)
					if prop:
						print prop
			else:
				print info
		else:
			print "ERROR getting the VM info: " + vm_id
			print info

	elif operation == "getinfo":
		inf_id = get_inf_id(args)
		propiedad = None
		if len(args) >= 2:
			propiedad = args[1]

		(success, res) = server.GetInfrastructureInfo(inf_id, auth_data)

		if success:
			vm_ids = res['vm_list']

			for vm_id in vm_ids:
				print "Info about VM with ID: " + vm_id
				(success, info)  = server.GetVMInfo(inf_id, vm_id, auth_data)

				if success:
					if propiedad == None:
						print info
					elif propiedad == 'state':
						print info['state']
					elif propiedad == 'radl':
						print info['info']
					elif propiedad == 'cloud':
						print info['cloud']
					else:
						info_radl = radl_parse.parse_radl(info['info'])
						for system in info_radl.systems:
							prop = system.getValue(propiedad)
							if prop:
								print prop
				else:
					print "ERROR getting the information about the VM: " + vm_id
					print info
		else:
			print "ERROR getting the information about the infrastructure: " + str(id)
			sys.exit(1)
	
	elif operation == "destroy":
		inf_id = get_inf_id(args)
		(success, inf_id) = server.DestroyInfrastructure(inf_id, auth_data)

		if success:
			print "Infrastructure destroyed"
		else:
			print "ERROR destroying the infrastructure: " + inf_id
			sys.exit(1)
			
	elif operation == "list":
		(success, res) = server.GetInfrastructureList(auth_data)

		if success:
			print res
		else:
			print "ERROR listing then infrastructures: " + res
			sys.exit(1)

	elif operation == "start":
		inf_id = get_inf_id(args)
		(success, inf_id) = server.StartInfrastructure(inf_id, auth_data)

		if success:
			print "Infrastructure started"
		else:
			print "ERROR starting the infraestructure: " + inf_id
			sys.exit(1)
			
	elif operation == "stop":
		inf_id = get_inf_id(args)
		(success, inf_id) = server.StopInfrastructure(inf_id, auth_data)

		if success:
			print "Infrastructure stopped"
		else:
			print "ERROR stopping the infrastructure: " + inf_id
			sys.exit(1)
