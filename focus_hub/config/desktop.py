from frappe import _

def get_data():
	return [
		{
			"module_name": "Focus Hub",
			"label": _("Focus Hub"),
			"type": "module",
			"icon": "octicon octicon-briefcase"
		},
		{
			"module_name": "Faktúry",
			"label": _("Faktúry"),
			"type": "module",
			"icon": "octicon octicon-file-directory"
		},
		{
			"module_name": "Vystavené Faktúry",
			"label": _("Vystavené Faktúry"),
			"type": "module",
			"icon": "octicon octicon-file-submodule"
		},
		{
			"module_name": "Prijaté Faktúry",
			"label": _("Prijaté Faktúry"),
			"type": "module",
			"icon": "octicon octicon-file-submodule"
		},
		{
			"module_name": "Výdavky",
			"label": _("Výdavky"),
			"type": "module",
			"icon": "octicon octicon-file-submodule"
		},
		{
			"module_name": "Členovia",
			"label": _("Členovia"),
			"type": "module",
			"icon": "octicon octicon-organization"
		}
	]
