#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import itertools as it, operator as op, functools as ft
from os.path import dirname, basename, exists, isdir, join, abspath
from posixpath import join as ujoin, dirname as udirname, basename as ubasename
from collections import defaultdict
import os, sys, io, re, types, json

try:
	import chardet
except ImportError: # optional
	chardet = None

try:
	from onedrive import api_v5, conf
except ImportError:
	# Make sure it works from a checkout
	if isdir(join(dirname(__file__), 'onedrive')) \
		and exists(join(dirname(__file__), 'setup.py')):
		sys.path.insert(0, dirname(__file__))
		from onedrive import api_v5, conf
	else:
		import api_v5, conf


force_encoding = None

def tree_node(): return defaultdict(tree_node)

def print_result(data, file, indent='', indent_first=None, indent_level=' '*2):
	# Custom printer is used because pyyaml isn't very pretty with unicode
	if isinstance(data, list):
		for v in data:
			print_result(v, file=file, indent=indent + '  ',
				indent_first=(indent_first if indent_first is not None else indent) + '- ')
			indent_first = None
	elif isinstance(data, dict):
		indent_cur = indent_first if indent_first is not None else indent
		for k, v in sorted(data.viewitems(), key=op.itemgetter(0)):
			print(indent_cur + decode_obj(k, force=True) + ':', file=file, end='')
			indent_cur = indent
			if not isinstance(v, (list, dict)): # peek to display simple types inline
				print_result(v, file=file, indent=' ')
			else:
				print('', file=file)
				print_result(v, file=file, indent=indent_cur+indent_level)
	else:
		if indent_first is not None: indent = indent_first
		print(indent + decode_obj(data, force=True), file=file)

def decode_obj(obj, force=False):
	'Convert or dump object to unicode.'
	if isinstance(obj, unicode):
		return obj
	elif isinstance(obj, bytes):
		if force_encoding is not None:
			return obj.decode(force_encoding)
		if chardet:
			enc_guess = chardet.detect(obj)
			if enc_guess['confidence'] > 0.7:
				return obj.decode(enc_guess['encoding'])
		return obj.decode('utf-8')
	else:
		return obj if not force else repr(obj)


def size_units(size,
			_units=list(reversed(list((u, 2 ** (i * 10)) #!as3
				for i, u in enumerate('BKMGT')))) ): #!as3
	for u, u1 in _units:
		if size > u1: break
	return size / float(u1), u


def id_match( s,
			_re_id=re.compile(r'^(file|folder)\.[0-9a-f]{16}\.[0-9A-F]{16}!\d+|folder\.[0-9a-f]{16}$') ): #!as2
	return s if s and _re_id.search(s) else None


def main():
	import argparse

	parser = argparse.ArgumentParser(
		description='Tool to manipulate OneDrive contents.')
	parser.add_argument('-c', '--config',
						metavar='path', default=conf.ConfigMixin.conf_path_default,
						help='Writable configuration state-file (yaml).'
							' Used to store authorization_code, access and refresh tokens.' #!as1
							' Should initially contain at least something like "{client: {id: xxx, secret: yyy}}".' #!as1
							' Default: %(default)s') #!as1

	parser.add_argument('-p', '--path', action='store_true',
						help='Interpret file/folder arguments only as human paths, not ids (default: guess).'
							' Avoid using such paths if non-unique "name" attributes' #!as1
							' of objects in the same parent folder might be used.') #!as1
	parser.add_argument('-i', '--id', action='store_true',
						help='Interpret file/folder arguments only as ids (default: guess).')

	parser.add_argument('-e', '--encoding', metavar='enc',
						action='store', help='Use specified encoding (example: utf-8) for CLI input/output.'
							' See full list of supported encodings at:' #!as1
								' http://docs.python.org/2/library/codecs.html#standard-encodings .' #!as1
							' Default behavior is to detect input encoding via chardet module,' #!as1
								' if available, falling back to utf-8 and use terminal encoding for output.') #!as1

	parser.add_argument('--debug',
						action='store_true', help='Verbose operation mode.')

	cmds = parser.add_subparsers(title='Supported operations')

	def add_command(name, **kwz):
		cmd = cmds.add_parser(name, **kwz)
		cmd.set_defaults(call=name)
		return cmd

	cmd = add_command('auth', help='Perform user authentication.')
	cmd.add_argument('url', nargs='?',
					help='URL with the authorization_code.') #!as1

	add_command('quota', help='Print quota information.')
	add_command('recent', help='List recently changed objects.')

	cmd = add_command('info', help='Display object metadata.')
	cmd.add_argument('object',
					nargs='?', default='me/skydrive', #!as1
					help='Object to get info on (default: %(default)s).') #!as1

	cmd = add_command('info_set', help='Manipulate object metadata.')
	cmd.add_argument('object',
					help='Object to manipulate metadata for.') #!as1
	cmd.add_argument('data',
					help='JSON mapping of values to set' #!as1
						' (example: {"name": "new_file_name.jpg"}).') #!as2

	cmd = add_command('link', help='Get a link to a file.')
	cmd.add_argument('object', help='Object to get link for.')
	cmd.add_argument('-t', '--type', default='shared_read_link',
					help='Type of link to request. Possible values' #!as1
						' (default: %(default)s): shared_read_link, embed, shared_edit_link.') #!as2

	cmd = add_command('ls', help='List folder contents.')
	cmd.add_argument('folder',
					nargs='?', default='me/skydrive', #!as1
					help='Folder to list contents of (default: %(default)s).') #!as1
	cmd.add_argument('-r', '--range', metavar='{[offset]-[limit] | limit}',
					help='List only specified range of objects inside.'
						' Can be either dash-separated "offset-limit" tuple' #!as1
						' (any of these can be omitted) or a single "limit" number.') #!as1
	cmd.add_argument('-o', '--objects', action='store_true',
					help='Dump full objects, not just name and id.') #!as1

	cmd = add_command('mkdir', help='Create a folder.')
	cmd.add_argument('name',
					help='Name (or a path consisting of dirname + basename) of a folder to create.') #!as1
	cmd.add_argument('folder',
					nargs='?', default=None, #!as1
					help='Parent folder (default: me/skydrive).') #!as1
	cmd.add_argument('-m', '--metadata',
					help='JSON mappings of metadata to set for the created folder.' #!as1
						' Optonal. Example: {"description": "Photos from last trip to Mordor"}') #!as2

	cmd = add_command('get', help='Download file contents.')
	cmd.add_argument('file', help='File (object) to read.')
	cmd.add_argument('file_dst', nargs='?', help='Name/path to save file (object) as.')
	cmd.add_argument('-b', '--byte-range',
					help='Specific range of bytes to read from a file (default: read all).' #!as1
						' Should be specified in rfc2616 Range HTTP header format.' #!as2
						' Examples: 0-499 (start - 499), -500 (end-500 to end).') #!as2

	cmd = add_command('put', help='Upload a file.')
	cmd.add_argument('file', help='Path to a local file to upload.')
	cmd.add_argument('folder',
					nargs='?', default='me/skydrive', #!as1
					help='Folder to put file into (default: %(default)s).') #!as1
	cmd.add_argument('-n', '--no-overwrite', action='store_true',
					help='Do not overwrite existing files with the same "name" attribute (visible name).') #!as1
	cmd.add_argument('-d', '--no-downsize', action='store_true',
					help='Disable automatic downsizing when uploading a photo.') #!as1

	cmd = add_command('cp', help='Copy file to a folder.')
	cmd.add_argument('file', help='File (object) to copy.')
	cmd.add_argument('folder',
					nargs='?', default='me/skydrive', #!as1
					help='Folder to copy file to (default: %(default)s).') #!as1

	cmd = add_command('mv', help='Move file to a folder.')
	cmd.add_argument('file', help='File (object) to move.')
	cmd.add_argument('folder',
					nargs='?', default='me/skydrive', #!as1
					help='Folder to move file to (default: %(default)s).') #!as1

	cmd = add_command('rm', help='Remove object (file or folder).')
	cmd.add_argument('object', nargs='+', help='Object(s) to remove.')

	cmd = add_command('comments', help='Show comments for a file, object or folder.')
	cmd.add_argument('object', help='Object to show comments for.')

	cmd = add_command('comment_add', help='Add comment for a file, object or folder.')
	cmd.add_argument('object', help='Object to add comment for.')
	cmd.add_argument('message', help='Comment message to add.')

	cmd = add_command('comment_delete', help='Delete comment from a file, object or folder.')
	cmd.add_argument('comment_id',
					help='ID of the comment to remove (use "comments"' #!as1
						' action to get comment ids along with the messages).') #!as2

	cmd = add_command('tree',
					help='Show contents of onedrive (or folder) as a tree of file/folder names.' #!as2
						' Note that this operation will have to (separately) request a listing' #!as3
						' of every folder under the specified one, so can be quite slow for large' #!as3
						' number of these.') #!as3
	cmd.add_argument('folder',
					nargs='?', default='me/skydrive', #!as1
					help='Folder to display contents of (default: %(default)s).') #!as1
	cmd.add_argument('-o', '--objects', action='store_true',
					help='Dump full objects, not just name and type.') #!as1

	optz = parser.parse_args()

	if optz.path and optz.id:
		parser.error('--path and --id options cannot be used together.')

	if optz.encoding:
		global force_encoding
		force_encoding = optz.encoding

		import codecs
		sys.stdin = codecs.getreader(optz.encoding)(sys.stdin)
		sys.stdout = codecs.getwriter(optz.encoding)(sys.stdout)

	import logging

	log = logging.getLogger()
	logging.basicConfig(level=logging.WARNING
	if not optz.debug else logging.DEBUG)

	api = api_v5.PersistentOneDriveAPI.from_conf(optz.config)
	res = xres = None
	resolve_path = ( (lambda s: id_match(s) or api.resolve_path(s)) \
						if not optz.path else api.resolve_path ) if not optz.id else lambda obj_id: obj_id #!as1

	# Make best-effort to decode all CLI options to unicode
	for k, v in vars(optz).viewitems():
		if isinstance(v, bytes):
			setattr(optz, k, decode_obj(v))
		elif isinstance(v, list):
			setattr(optz, k, map(decode_obj, v))

	if optz.call == 'auth':
		if not optz.url:
			print('Visit the following URL in any web browser (firefox, chrome, safari, etc),\n'
				'  authorize there, confirm access permissions, and paste URL of an empty page\n' #!as2
				'  (starting with "https://login.live.com/oauth20_desktop.srf")' #!as2
				' you will get redirected to in the end.') #!as2
			print('Alternatively, use the returned (after redirects)'
				' URL with "{} auth <URL>" command.\n'.format(sys.argv[0])) #!as2
			print('URL to visit: {}\n'.format(api.auth_user_get_url()))
			optz.url = raw_input('URL after last redirect: ').strip()
		if optz.url:
			api.auth_user_process_url(optz.url)
			api.auth_get_token()
			print('API authorization was completed successfully.')

	elif optz.call == 'quota':
		df, ds = map(size_units, api.get_quota())
		res = dict(free='{:.1f}{}'.format(*df), quota='{:.1f}{}'.format(*ds))
	elif optz.call == 'recent':
		res = api('me/skydrive/recent_docs')['data']

	elif optz.call == 'ls':
		offset = limit = None
		if optz.range:
			span = re.search(r'^(\d+)?[-:](\d+)?$', optz.range)
			try:
				if not span:
					limit = int(optz.range)
				else:
					offset, limit = map(int, span.groups())
			except ValueError:
				parser.error('--range argument must be in the "[offset]-[limit]"'
							' or just "limit" format, with integers as both offset and' #!as1
							' limit (if not omitted). Provided: {}'.format(optz.range)) #!as1
		res = list(api.listdir(resolve_path(optz.folder), offset=offset, limit=limit))
		if not optz.objects: res = map(op.itemgetter('name'), res)

	elif optz.call == 'info':
		res = api.info(resolve_path(optz.object))
	elif optz.call == 'info_set':
		xres = api.info_update(
			resolve_path(optz.object), json.loads(optz.data))
	elif optz.call == 'link':
		res = api.link(resolve_path(optz.object), optz.type)
	elif optz.call == 'comments':
		res = api.comments(resolve_path(optz.object))
	elif optz.call == 'comment_add':
		res = api.comment_add(resolve_path(optz.object), optz.message)
	elif optz.call == 'comment_delete':
		res = api.comment_delete(optz.comment_id)

	elif optz.call == 'mkdir':
		name, path = optz.name.replace('\\', '/'), optz.folder
		if '/' in name:
			name, path_ext = ubasename(name), udirname(name)
			path = ujoin(path, path_ext.strip('/')) if path else path_ext
		xres = api.mkdir(name=name, folder_id=resolve_path(path),
						metadata=optz.metadata and json.loads(optz.metadata) or dict()) #!as1

	elif optz.call == 'get':
		contents = api.get(resolve_path(optz.file), byte_range=optz.byte_range)
		if optz.file_dst:
			dst_dir = dirname(abspath(optz.file_dst))
			if not isdir(dst_dir):
				os.makedirs(dst_dir)
			with open(optz.file_dst, "wb") as dst:
				dst.write(contents)
		else:
			sys.stdout.write(contents)
			sys.stdout.flush()

	elif optz.call == 'put':
		xres = api.put(optz.file,
					resolve_path(optz.folder), #!as3
					overwrite=not optz.no_overwrite, #!as3
					downsize=not optz.no_downsize) #!as3

	elif optz.call in ['cp', 'mv']:
		argz = map(resolve_path, [optz.file, optz.folder])
		xres = (api.move if optz.call == 'mv' else api.copy)(*argz)

	elif optz.call == 'rm':
		for obj in it.imap(resolve_path, optz.object): xres = api.delete(obj)


	elif optz.call == 'tree':

		def recurse(obj_id):
			node = tree_node()
			for obj in api.listdir(obj_id):
				# Make sure to dump files as lists with -o,
				#  not dicts, to make them distinguishable from dirs
				res = obj['type'] if not optz.objects else [obj['type'], obj]
				node[obj['name']] = recurse(obj['id']) \
					if obj['type'] in ['folder', 'album'] else res
			return node

		root_id = resolve_path(optz.folder)
		res = {api.info(root_id)['name']: recurse(root_id)}


	else:
		parser.error('Unrecognized command: {}'.format(optz.call))

	if res is not None: print_result(res, file=sys.stdout)
	if optz.debug and xres is not None:
		buff = io.StringIO()
		print_result(xres, file=buff)
		log.debug('Call result:\n{0}\n{1}{0}'.format('-' * 20, buff.getvalue()))


if __name__ == '__main__': main()
