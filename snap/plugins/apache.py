import subprocess
import snapcraft.plugins.v1


class ApachePlugin(snapcraft.plugins.v1.PluginV1):

    @classmethod
    def schema(cls):
        schema = super().schema()

        schema['properties']['modules'] = {
            'type': 'array',
            'minitems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string'
            },
        }

        schema['properties']['mpm'] = {
            'type': 'string',
            'default': 'event',
        }

        schema['required'] = ['modules']

        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)

        self.build_packages.extend(
            ['pkg-config', 'libapr1-dev', 'libaprutil1-dev', 'libpcre3-dev',
             'libssl-dev'])
        self.stage_packages.extend(['libapr1', 'libaprutil1'])

    def build(self):
        super().build()

        subprocess.check_call(
            "./configure --prefix={} --with-mpm={} --enable-modules=none --enable-mods-shared='{}' ENABLED_DSO_MODULES='{}'".format(
                self.installdir, self.options.mpm,
                ' '.join(self.options.modules),
                ','.join(self.options.modules)),
            cwd=self.builddir, shell=True)

        self.run(
            ['make', '-j{}'.format(
                self.project.parallel_build_count)],
            cwd=self.builddir)
        self.run(['make', 'install'], cwd=self.builddir)
