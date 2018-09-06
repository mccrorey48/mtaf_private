import re
from ePhone7.lib.utils.spud_serial import SpudSerial
from ePhone7.config.configure import cfg
import spur
from mtaf.user_exception import UserException as Ux
from mtaf.decorators import Trace
from mtaf import mtaf_logging
from mtaf.ADB import ADB
from mtaf.Fastboot import Fastboot
from os import path, listdir, mkdir
import shutil

log = mtaf_logging.get_logger('mtaf.versions')

__all__ = ['get_installed_versions', 'force_aosp_downgrade', 'remove_apk_upgrades', 'get_current_versions']


@Trace(log)
def get_installed_versions():
    re_aosp = re.compile('\[ro\.build\.id\]:\s+\[(.*)\]')
    re_apk = re.compile('(?ms).*Packages:.*?versionName=(\d+\.\d+\.\d+)')
    action = {'cmd': 'getprop\n', 'timeout': 10}
    aosp_version = None
    apk_version = None
    log.debug("Creating SpudSerial device")
    ss = SpudSerial(cfg.site['SerialDev'])
    log.debug("Flushing SpudSerial device")
    ss.flush(1)
    log.debug("SpudSerial device created")
    (reply, elapsed, groups) = ss.do_action(action)
    for line in reply.split('\n'):
        if re_aosp.match(line):
            aosp_version = re_aosp.match(line).group(1)
    adb = ADB()
    m = re_apk.match(adb.run_cmd('shell dumpsys package com.esi_estech.ditto'))
    if m:
        apk_version = m.group(1)
    return aosp_version, apk_version


@Trace(log)
def remove_apk_upgrades():
    ss = SpudSerial(cfg.site['SerialDev'])
    action = {'cmd': 'pm uninstall com.esi_estech.ditto\n', 'expect': 'Success|Failure', 'timeout': 20}
    while True:
        (reply, elapsed, groups) = ss.do_action(action)
        if groups[0] == 'Failure':
            break


@Trace(log)
def get_current_versions(ota_server):
    build_prop_server = cfg.site["BuildPropServer"]
    # get the current version from the build server
    shell = spur.SshShell(
        hostname=build_prop_server,
        username='ubuntu',
        private_key_file='ePhone7/keys/OTAServer2.pem',
        missing_host_key=spur.ssh.MissingHostKey.accept
    )
    with shell:
        result = shell.run(['cat', '/www/aus/releases/%s/build.prop' % ota_server])
    current_aosp = None
    current_app = None
    aosp_prefix = 'ro.build.id='
    aosp_new_prefix = 'system.version='
    app_prefix = 'app.version='
    for line in result.output.split('\n'):
        line = line.strip()
        if line.startswith(aosp_prefix):
            current_aosp = line[len(aosp_prefix):]
        elif line.startswith(aosp_new_prefix):
            current_aosp = line[len(aosp_new_prefix):]
        elif line.startswith(app_prefix):
            current_app = line[len(app_prefix):]
    if current_aosp is None:
        raise Ux("current_aosp not found")
    elif current_app is None:
        raise Ux("current_app not found")
    return current_aosp, current_app


@Trace(log)
def force_aosp_downgrade(version):
    actions = [
        {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'Hit any key to stop autoboot:', 'timeout': 30,
         'dead_air_timeout': 30},
        {'cmd': '\n', 'expect': '=> ', 'timeout': 5},
        {'cmd': 'mmc dev 2\n', 'expect': 'mmc2\(part 0\) is current device\n=> '},
        {'cmd': 'mmc setdsr 2\n', 'expect': 'set dsr OK, force rescan\n=> '},
        {'cmd': 'fastboot\n', 'expect': '0x4\nUSB_RESET\nUSB_PORT_CHANGE 0x4\n'}
    ]
    ss = SpudSerial(cfg.site['SerialDev'])
    for action in actions:
        (reply, elapsed, groups) = ss.do_action(action)
        log.debug('[%5.3fs] cmd %s, expect %s, received %d chars'
                  % (elapsed, repr(action['cmd']), repr(action['expect']), len(reply)))
        ss.connection.reset_input_buffer()
    fb = Fastboot()
    fb_cmds = [
        "flash boot %s" % path.join(cfg.site["AospsHome"], version, "boot.img"),
        "flash system %s" % path.join(cfg.site["AospsHome"], version, "system.img"),
        "flash recovery %s" % path.join(cfg.site["AospsHome"], version, "recovery.img"),
        "reboot"
    ]
    for cmd in fb_cmds:
        log.debug(">>> fastboot " + cmd)
        log.debug(fb.run_cmd(cmd))
    ss.do_action({'cmd': '', 'new_cwd': '', 'expect': 'mtp_open', 'timeout': 600, 'dead_air_timeout': 60})


@Trace(log)
def force_app_downgrade(version):
    ss = SpudSerial(cfg.site['SerialDev'])
    adb = ADB()
    log.debug(adb.run_cmd("install -r -d %s.apk" % path.join(cfg.site["ApksHome"], version)).encode('string_escape'))
    action = {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'mtp_open', 'timeout': 120}
    ss.do_action(action)


@Trace(log)
def get_downgrade_images(downgrade_aosp, downgrade_app=None):
    build_image_server = cfg.site["BuildImageServer"]
    aosps_home = cfg.site["AospsHome"]
    apks_home = cfg.site["ApksHome"]

    # make sure both aosps_home and apks_home directories exist
    try:
        mkdir(aosps_home)
    except OSError:
        pass
    try:
        mkdir(apks_home)
    except OSError:
        pass

    # make sure the downgrade versions of the aosp and apk are available
    aosp_dirs = listdir(aosps_home)
    apks = listdir(apks_home)
    if downgrade_aosp not in aosp_dirs:
        mkdir(path.join(aosps_home, downgrade_aosp))
    shell = spur.SshShell(
        hostname=build_image_server,
        username='root',
        password='root',
        missing_host_key=spur.ssh.MissingHostKey.accept
    )
    aosp_downgrade_images = listdir(path.join(aosps_home, downgrade_aosp))
    with shell:
        for basename in ['boot', 'system', 'recovery']:
            img_filename = basename + '.img'
            remote_img_path = 'aosps/%s/%s' % ('_'.join(['build'] + downgrade_aosp.split('.')), img_filename)
            print "remote file: " + remote_img_path
            local_img_path = path.join(aosps_home, downgrade_aosp, img_filename)
            print "local file: " + local_img_path + '...',
            if img_filename in aosp_downgrade_images:
                print "already downloaded to test host"
            else:
                print "downloading to test host"
                with shell.open(remote_img_path, 'rb') as remote_file:
                    with open(local_img_path, 'wb') as local_file:
                        shutil.copyfileobj(remote_file, local_file)
        if downgrade_app is not None:
            remote_apk_filename = 'update.apk.%02d%02d%02d' % tuple([int(n) for n in downgrade_app.split('.')])
            local_apk_filename = downgrade_app + '.apk'
            remote_apk_path = 'apks/' + remote_apk_filename
            local_apk_path = path.join(apks_home, local_apk_filename)
            print "remote file: " + remote_apk_path
            print "local file: " + remote_apk_path + '...',
            if local_apk_filename in apks:
                print "already downloaded to test host"
            else:
                print "downloading to test host"
                with shell.open(remote_apk_path, 'rb') as remote_file:
                    with open(local_apk_path, 'wb') as local_file:
                        shutil.copyfileobj(remote_file, local_file)


