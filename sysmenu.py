#!/usr/bin/python
from configparser import ConfigParser
from os.path import expanduser
from subprocess import check_output, Popen
from sys import argv

from tkinter import Frame, SINGLE, Tk
from tkinter import Button, Label

if len(argv) != 2:
	print("sysmenu: invalid number of arguments")
	exit(1)

menu = f'menu:{argv[1]}'

config = ConfigParser()
config.read(expanduser('~/.config/sysmenu/config'))

x = config[menu]['x'] or 0
y = config[menu]['y'] or 0

def get_config(section, key, globaldefault = True):
	if key in config[section]:
		return config[section][key]
	elif globaldefault and key in config['global']:
		return config['global'][key]
	else:
		return None

background	=	get_config(menu, 'background') or 'white'
foreground	=	get_config(menu, 'foreground') or 'black'
highlight	=	get_config(menu, 'highlight') or 'gray'
padding_x	=	get_config(menu, 'padding_x') or 0
padding_y	=	get_config(menu, 'padding_y') or 0

root = Tk()
root.title('sysmenu')
root.bind("<FocusOut>", exit)
root.bind("<Key>", exit)
root.geometry(f'+{x}+{y}')

if background is not None:
	root.configure(background = background);

components = []

def run(command):
	Popen(command, shell = True)
	exit()

def beval(expression, striptype = 'both'):
	output = check_output(f'echo "{expression}"', shell = True).decode('utf-8')
	if striptype == 'both':
		return output.strip()
	elif striptype == 'right':
		return output.rstrip()
	elif striptype == 'left':
		return output.lstrip()
	elif striptype == 'none':
		return output
	else:
		print(f'sysmenu: invalid strip type "{striptype}"; must be "both", "right", "left", or "none".')
		exit(1)

def font(name):
	sec = f'font:{name}'
	if sec not in config:
		print(f'sysmenu: no font "{name}" (section "{sec}" missing)')
	fontinfo = config[sec]
	return (fontinfo['family'], fontinfo['size'])

def make_button(name: str):
	spec = config[name]
	text = spec['text']
	if 'eval' in spec and bool(spec['eval']):
		if 'strip' in spec:
			text = beval(text, spec['strip'])
		else:
			text = beval(text)
	button = Button(
		root,
		text = text,
		command = lambda: run(spec['command'])
	)
	button.configure(
		borderwidth = 0,
		highlightthickness = 0,
		bg = background,
		fg = foreground,
		activeforeground = foreground,
		activebackground = highlight,
		padx = padding_x,
		pady = padding_y
	)
	if 'font' in spec:
		button.configure(font = font(spec['font']))
	if 'condition' in spec:
		state = beval(spec['condition']);
		if state.lower() != "true":
			button['state'] = 'disabled'
	components.append(button)

def make_label(name: str):
	spec = config[name]
	text = spec['text']
	if 'eval' in spec and bool(spec['eval']):
		if 'strip' in spec:
			text = beval(text, spec['strip'])
		else:
			text = beval(text)
	label = Label(
		root,
		text = text
	)
	label.configure(
		borderwidth = 0,
		highlightthickness = 0,
		bg = background,
		fg = foreground,
		padx = padding_x,
		pady = padding_y
	)
	if 'font' in spec:
		label.configure(font = font(spec['font']))
	components.append(label)

items = config[menu]['items'].split()
for item in items:
	if item.startswith('button:'):
		make_button(item)
	if item.startswith('label:'):
		make_label(item)

for item in components:
	item.pack(fill = 'x')
root.mainloop()
