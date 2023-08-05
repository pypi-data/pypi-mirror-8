# coding: utf-8
# flake8: noqa

import os
import subprocess
import re
import yaml
import shutil
from termcolor import colored

__have_vagrant__ = True
__vagrant_unavailable_msg__ = "Vagrant is not available. Please install vagrant from http://vagrantup.com and try again."

try:
    import vagrant
except ImportError:
    __have_vagrant__ = False
except  AssertionError:
    __have_vagrant__ = False

import nepho
from nepho.core.common import cwd, execute

class VagrantProvider(nepho.core.provider.AbstractProvider):
    """An infrastructure provider class for Vagrant"""

    PROVIDER_ID = "vagrant"
    TEMPLATE_FILENAME = "Vagrantfile"

    def __init__(self, config, scenario=None):

        if __have_vagrant__ is not True:
            print colored("Error: ", "red") + __vagrant_unavailable_msg__
            exit(1)

        nepho.core.provider.AbstractProvider.__init__(self, config, scenario)
        self.params = {
            'VagrantBackend': 'virtualbox',
            'BoxName': None
        }

        if scenario is not None:
            if scenario.name is not None:
                self.stack_name = scenario.name
            else:
                context = scenario.context
                self.stack_name = "%s-%s" % (context['cloudlet']['name'],
                                             context['blueprint']['name'])
        else:
            print "scenario is none"

    @property
    def vagrantfile_path(self):
        # Lazy-load path because it requires a valid context.
        return os.path.join(
            self.scenario.context['cloudlet']['path'], 'resources',
            self.scenario.context['blueprint']['name'])

    @property
    def payload_path(self):
        return os.path.join(
            self.scenario.context['cloudlet']['path'], 'payload')

    @property
    def vagrant_backend(self):
        context = self.scenario.context
        if context['parameters']['VagrantBackend'] is None:
            print colored("Error: ", "red"), "Vagrant requires a valid backend provider, such as 'virtualbox'."
            print "Use \"nepho parameter set VagrantBackend <value>\" to set a parameter."
            exit(1)
        return context['parameters']['VagrantBackend']

    def validate_template(self, template_str):
        return "Validation:\n  Vagrant does not support validation."

    def create(self, app_obj):
        """Deploy a given pattern."""
        if app_obj.pargs.debug is True:
            print "Vagrant does not support debug logging"

        context = self.scenario.context
        raw_template = self.scenario.template
        working_path = self._working_path(app_obj)

        if os.path.isdir(working_path):
            print colored("Error: ", "red") + "Working directory already exists"
            print "Either a stack of this name is already running or an orphaned directory exists."
            exit(1)

        # Download box if it is not installed
        if context['parameters']['BoxName'] is not None:
            name = context['parameters']['BoxName']
            url = context['parameters']['BoxUrl']

            if name not in self._list_box_names(self.vagrant_backend):
                try:
                    print " - Downloading box %s" % (name)
                    execute('vagrant box add %s %s' % (name, url))
                except subprocess.CalledProcessError:
                    print colored("Error: ", "red") + 'Attempt to download box exited with a non-zero exit code.'
                    exit(1)

        try:
            if app_obj.pargs.develop is True:
                print " -", colored("Development mode:", "yellow"), "Symlinking payload to working directory"
                os.mkdir(working_path)
                os.symlink(self.payload_path, os.path.join(working_path, 'payload'))
            else:
                print " - Copying payload to working directory"
                shutil.copytree(self.payload_path, os.path.join(working_path, 'payload'))
        except:
            print colored("Error: ", "red") + "Unable to create payload directory"
            shutil.rmtree(working_path)
            exit(1)

        print " - Generating Vagrantfile"
        try:
            f = open(os.path.join(working_path, 'Vagrantfile'), 'w')
            f.write(raw_template)
            f.close()
        except:
            print colored("Error: ", "red") + "Unable to generate Vagrantfile"
            exit(1)

        with cwd(working_path):
            #v = vagrant.Vagrant()
            vm_name = None
            try:
                print " - Running Vagrant from: %s" % (working_path)
                print ""
                #v.up(provider=self.vagrant_backend, vm_name=vm_name)
                execute('vagrant up')
                print 'Vagrant run complete. Run "nepho stack status" for details or "nepho stack access" to connect.'
            except subprocess.CalledProcessError:
                print colored("Error: ", "red") + 'Vagrant exited with a non-zero exit code, but your VM may be running.  Run "nepho stack status" for details.'

    def update(self, app_obj):
        if app_obj.pargs.debug is True:
            print "Vagrant does not support debug logging"

        context = self.scenario.context
        raw_template = self.scenario.template
        working_path = self._working_path(app_obj)

        if not os.path.isdir(working_path):
            print colored("Error: ", "red") + "Working directory does not exist"
            print "Update can only be run on a running stack."
            exit(1)

        try:
            if app_obj.pargs.develop is True:
                print " -", colored("Development mode:", "yellow"), "Not updating payload"
            else:
                print " - Deleting old payload from working directory"
                shutil.rmtree(os.path.join(working_path, 'payload'))
                print " - Copying payload to working directory"
                shutil.copytree(self.payload_path, os.path.join(working_path, 'payload'))
        except:
            print colored("Error: ", "red") + "Unable to update payload directory"
            exit(1)

        with cwd(working_path):
            vm_name = None
            try:
                execute('vagrant provision')
            except subprocess.CalledProcessError:
                print colored("Error: ", "red") + 'Vagrant provision exited with a non-zero exit code.'

    def status(self, app_obj):
        working_path = self._working_path(app_obj)

        if not os.path.isdir(working_path):
            print colored("Error: ", "red") + "Working directory does not exist"
            exit(1)
        else:
            with cwd(working_path):
                v = vagrant.Vagrant()
                instances = v.status()

                print "Name:        %s" % self.stack_name
                print "Working Dir: %s" % working_path
                print
                print colored(" %-32s %-24s " % ("Instance", "Status"), 'white', 'on_blue')
                for k, v in instances.items():
                    print " %-32s %-24s " % (k, v)

                print "\nTo run Vagrant commands directly, change to the working directory listed above.\n"

    def access(self, app_obj):
        if not os.path.isdir(self._working_path(app_obj)):
            print colored("Error: ", "red") + "Working directory does not exist"
            exit(1)
        else:
            with cwd(self._working_path(app_obj)):
                v = vagrant.Vagrant()
                ssh_connect_string = v.user_hostname_port()
                vagrant_binary = vagrant.VAGRANT_EXE
                os.execlp(vagrant_binary, "", "ssh")

    def destroy(self, app_obj):
        if not os.path.isdir(self._working_path(app_obj)):
            print colored("Error: ", "red") + "Working directory does not exist"
            exit(1)
        else:
            with cwd(self._working_path(app_obj)):
                try:
                    v = vagrant.Vagrant()
                    print " - Terminating instance(s)"
                    v.destroy()
                finally:
                    print " - Removing working directory"
                    if app_obj.pargs.develop is True:
                        os.unlink(os.path.join(working_path, 'payload'))
                    shutil.rmtree(self._working_path(app_obj))

    def _list_boxes(self):
        listing = subprocess.check_output('vagrant box list', shell=True)
        boxes = []
        for line in listing.splitlines():
            m = re.search(r'^\s*(?P<name>.+?)\s+\((?P<provider>[^)]+)\)\s*$', line)
            if m:
                boxes.append((m.group('name'), m.group('provider')))
        return boxes

    def _list_box_names(self, backend):
        return [box[0] for box in self._list_boxes() if box[1] == backend]

    def _working_path(self, app_obj):
        return os.path.join(app_obj.config.get('nepho', 'working_dir'), self.stack_name)

