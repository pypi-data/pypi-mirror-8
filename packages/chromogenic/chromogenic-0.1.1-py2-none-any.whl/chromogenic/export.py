import os

#from chromogenic.clean import remove_ldap, remove_vnc, remove_sensu
from chromogenic.common import prepare_chroot_env, remove_chroot_env,\
                                   run_command,\
                                   rebuild_ramdisk,\
                                   append_line_in_files,\
                                   prepend_line_in_files,\
                                   replace_line_in_files
from chromogenic.common import sed_replace


def export_instance(src_managerCls, src_manager_creds, exportCls, **export_args):
    """
    Use the source manager to download a local image file
    Then start the export by passing the image to exportCls
    """
    #Download the image
    download_manager = src_managerCls(**src_manager_creds)
    download_kwargs = src_manager.download_instance_args(**export_args)
    download_location = src_manager.download_instance(**download_kwargs)
    #Clean the image (Optional)
    download_dir = os.path.dirname(download_location)
    mount_point = os.path.join(download_dir, 'mount_point/')
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)
    if export_args.get('clean_image',True):
        src_manager.mount_and_clean(
                download_location,
                mount_point,
                **export_args)
    export_args['download_location'] = download_location
    export_manager = migrationCls(**migration_creds)
    #Add required files/make necessary changes for export..
    export_manager.mount_and_clean(
            download_location,
            mount_point,
            **export_args)
    image_location = export_manager.rebuild_disk(download_location, **export_args)
    export_args['download_location'] = image_location
    #Start the export
    #cleaned_export_args = export_manager.clean_export_args(**export_args)
    export_file = export_manager.export(**cleaned_export_args)
    return export_file

def add_virtualbox_support(mounted_path, image_path):
    """
    These configurations are specific to running virtualbox from an exported VM
    """
    #remove_ldap(mounted_path)
    #remove_vnc(mounted_path)
    #remove_sensu(mounted_path)

    add_gnome_support(mounted_path)

    #Touch to create a new module file
    new_mod_file = os.path.join(mounted_path, 'etc/modprobe.d/virtualbox')
    open(new_mod_file,'a').close()

    add_eth0_module(mounted_path)
    add_intel_soundcard(mounted_path)

    rebuild_ramdisk(mounted_path)


def add_gnome_support(mounted_path):
    """
    RHEL only at this point.
    TODO: Add ubuntu, then add deterine_distro code
    """
    prepare_chroot_env(mounted_path)
    run_command([
        "/usr/sbin/chroot", mounted_path, "/bin/bash", "-c", "yum groupinstall"
        " -y \"X Window System\" \"GNOME Desktop Environment\""])
    #Selinux was enabled in the process. lets fix that:
    selinux_conf = os.path.join(mounted_path, 'etc/sysconfig/selinux')
    sed_replace("SELINUX=enforcing", "SELINUX=disabled", selinux_conf)
    remove_chroot_env(mounted_path)

    #Make it the default on boot
    replace_line_file_list = [
         (":[0-6]:initdefault",":5:initdefault",
             "etc/inittab"),
    ]
    replace_line_in_files(replace_line_file_list, mounted_path)


def add_eth0_module(mounted_path):
    prepend_line_list = [
         ("alias eth0 e1000",
          "etc/modprobe.d/virtualbox"),
    ]
    prepend_line_in_files(prepend_line_list, mounted_path)


def add_intel_soundcard(mounted_path):
    append_line_list = [
        ("alias scsi_hostadapter1 ahci","etc/modprobe.d/modprobe.conf"),
        ("install pciehp /sbin/modprobe -q --ignore-install acpiphp; "
         "/bin/true","etc/modprobe.d/virtualbox"),
        ("alias snd-card-0 snd-intel8x0","etc/modprobe.d/modprobe.conf"),
        ("options snd-intel8x0 index=0","etc/modprobe.d/modprobe.conf"),
        ("options snd-card-0 index=0","etc/modprobe.d/modprobe.conf"),
        ("remove snd-intel8x0 { /usr/sbin/alsactl store 0 >/dev/null "
            "2>& 1 || : ; }; /sbin/modprobe -r --ignore-remove "
            "snd-intel8x0","etc/modprobe.d/virtualbox")
    ]
    append_line_in_files(append_line_list, mounted_path)

def remove_sensu(mounted_path):
    try:
        prepare_chroot_env(mounted_path)
        run_command(["/usr/sbin/chroot", mounted_path, 'yum',
                     'remove', '-qy', 'sensu'])
    finally:
        remove_chroot_env(mounted_path)

def remove_ldap(mounted_path, new_password='atmosphere'):
    try:
        prepare_chroot_env(mounted_path)
        run_command(["/usr/sbin/chroot", mounted_path, "/bin/bash", "-c",
                     "echo %s | passwd root --stdin" % new_password])
        run_command(["/usr/sbin/chroot", mounted_path, 'yum',
                     'remove', '-qy', 'openldap'])
    finally:
        remove_chroot_env(mounted_path)

def remove_vnc(mounted_path):
    try:
        prepare_chroot_env(mounted_path)
        run_command(["/usr/sbin/chroot", mounted_path, 'yum',
            'remove', '-qy', 'realvnc-vnc-server'])
        #remove rpmsave.. to get rid of vnc for good.
        #["/usr/sbin/chroot", mounted_path, 'find', '/',
        #'-type', 'f', '-name', '*.rpmsave', '-exec', 'rm', '-f',
        #'{}', ';']
    finally:
        remove_chroot_env(mounted_path)
