#-----------------------------
#Python example code:
#-----------------------------

import lvm

# Note: This example will create a logical unit, tag it and
# 	delete it, don't run this on production box!

#Dump information about PV
def print_pv(pv):
	print 'PV name: ', pv.getName(), ' ID: ' , pv.getUuid()	, 'Size: ' , pv.getSize()


#Dump some information about a specific volume group
def print_vg(h, vg_name):

	#Open read only
	vg = h.vgOpen(vg_name, 'r')

	print 'Volume group:', vg_name, 'Size: ', vg.getSize()

	#Retrieve a list of Physical volumes for this volume group
	pv_list = vg.listPVs()

	#Print out the physical volumes
	for p in pv_list:
		print_pv(p)

	#Get a list of logical volumes in this volume group
	lv_list = vg.listLVs()
	if len(lv_list):
		for l in lv_list:
			print 'LV name: ', l.getName(), ' ID: ', l.getUuid()
	else:
		print 'No logical volumes present!'

	vg.close()

#Returns the name of a vg with space available
def find_vg_with_free_space(h):
	free_space = 0
	rc = None

	vg_names = l.listVgNames()
	for v in vg_names:
		vg = h.vgOpen(v, 'r')
		c_free = vg.getFreeSize()
		if c_free > free_space:
			free_space = c_free
			rc = v
		vg.close()

	return rc

#Walk through the volume groups and fine one with space in which we can
#create a new logical volume
def create_delete_logical_volume(h):
	vg_name = find_vg_with_free_space(h)

	print 'Using volume group ', vg_name , ' for example'

	if vg_name:
		vg = h.vgOpen(vg_name, 'w')
		lv = vg.createLvLinear('python_lvm_ok_to_delete', vg.getFreeSize())

		if lv:
			print 'New lv, id= ' , lv.getUuid()

			#Create a tag
			lv.addTag('Demo_tag')

			#Get the tags
			tags = lv.getTags()
			for t in tags:
				#Remove tag
				lv.removeTag(t)

			lv.deactivate()
			lv.remove()

		vg.close()
	else:
		print 'No free space available to create demo lv!'

if __name__ == '__main__':
	#Create a new LVM instance
	l = lvm.Liblvm()

	#What version
	print 'lvm version=', l.getVersion()

	#Get a list of volume group names
	vg_names = l.listVgNames()

	#For each volume group display some information about each of them
	for vg_i in vg_names:
		print_vg(l, vg_i)

	#Demo creating a logical volume
	create_delete_logical_volume(l)

	#Close
	l.close()
