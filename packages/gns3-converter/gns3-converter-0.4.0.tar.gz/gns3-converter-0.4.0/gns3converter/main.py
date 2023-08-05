# Copyright (C) 2014 Daniel Lintott.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import json
import os
import shutil
import argparse
import logging
from gns3converter import __version__
from gns3converter.converter import Converter
from gns3converter.topology import JSONTopology

LOG_MSG_FMT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] ' \
              '%(message)s'
LOG_DATE_FMT = '%y%m%d %H:%M:%S'


def main():
    """
    Entry point for gns3-converter
    """
    print('GNS3 Topology Converter')

    arg_parse = setup_argparse()
    args = arg_parse.parse_args()

    if args.debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.WARNING

    logging.basicConfig(level=logging_level,
                        format=LOG_MSG_FMT, datefmt=LOG_DATE_FMT)

    logging.getLogger(__name__)

    # Add the main topology to the list of files to convert
    if args.topology == 'topology.net':
        args.topology = os.path.join(os.getcwd(), 'topology.net')

    topology_files = [{'file': topology_abspath(args.topology),
                       'snapshot': False}]

    # Add any snapshot topologies to be converted
    topology_files.extend(get_snapshots(args.topology))

    # Do the conversion
    for topology in topology_files:
        do_conversion(topology, args)


def setup_argparse():
    """
    Setup the argparse argument parser

    :return: instance of argparse
    :rtype: ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description='Convert old ini-style GNS3 topologies (<=0.8.7) to '
                    'the newer version 1+ JSON format')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('-n', '--name', help='Topology name (default uses the '
                                             'name of the old project '
                                             'directory)')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('topology', nargs='?', default='topology.net',
                        help='GNS3 .net topology file (default: topology.net)')
    parser.add_argument('--debug',
                        help='Enable debugging output',
                        action='store_true')
    return parser


def do_conversion(topology_def, args):
    """
    Convert the topology

    :param dict topology_def: Dict containing topology file and snapshot bool
    """
    # Create a new instance of the the Converter
    gns3_conv = Converter(topology_def['file'], args.debug)
    # Read the old topology
    old_top = gns3_conv.read_topology()
    new_top = JSONTopology()

    # Process the sections
    (topology) = gns3_conv.process_topology(old_top)

    # Generate the nodes
    new_top.nodes = gns3_conv.generate_nodes(topology)
    # Generate the links
    new_top.links = gns3_conv.generate_links(new_top.nodes)

    new_top.notes = gns3_conv.generate_notes(topology['artwork']['NOTE'])
    new_top.shapes = gns3_conv.generate_shapes(topology['artwork']['SHAPE'])
    new_top.images = gns3_conv.generate_images(topology['artwork']['PIXMAP'])

    # Enter topology name
    new_top.name = name(args)

    # Save the new topology
    save(args, gns3_conv, new_top, topology_def['snapshot'])


def topology_abspath(topology):
    """
    Get the absolute path of the topology file

    :param str topology: Topology file
    :return: Absolute path of topology file
    :rtype: str
    """
    return os.path.abspath(topology)


def topology_dirname(topology):
    """
    Get the directory containing the topology file

    :param str topology: topology file
    :return: directory which contains the topology file
    :rtype: str
    """
    return os.path.dirname(topology_abspath(topology))


def get_snapshots(topology):
    """
    Return the paths of any snapshot topologies

    :param str topology: topology file
    :return: list of dicts containing snapshot topologies
    :rtype: list
    """
    snapshots = []
    snap_dir = os.path.join(topology_dirname(topology), 'snapshots')
    if os.path.exists(snap_dir):
        snaps = os.listdir(snap_dir)
        for directory in snaps:
            snap_top = os.path.join(snap_dir, directory, 'topology.net')
            if os.path.exists(snap_top):
                snapshots.append({'file': snap_top,
                                  'snapshot': True})
    return snapshots


def name(args):
    """
    Calculate the name to save the converted topology as

    :return: new topology name
    :rtype: str
    """
    if args.name is not None:
        logging.debug('topology name supplied')
        topo_name = args.name
    else:
        logging.debug('topology name not supplied')
        topo_name = os.path.basename(topology_dirname(args.topology))
    return topo_name


def save(args, converter, json_topology, snapshot):
    """
    Save the converted topology

    :param args: Program arguments
    :param Converter converter: Converter instance
    :param JSONTopology json_topology: JSON topology layout
    :param bool snapshot: Snapshot Boolean
    """
    try:
        config_err = False
        image_err = False

        old_topology_dir = topology_dirname(converter.topology)

        if args.output:
            output_dir = os.path.abspath(args.output)
        else:
            output_dir = os.getcwd()

        topology_name = json_topology.name

        if snapshot:
            snapshot_name = os.path.basename(
                topology_dirname(converter.topology))
            output_dir = os.path.join(output_dir, 'snapshots', snapshot_name)
            topology_files_dir = os.path.join(output_dir, snapshot_name +
                                              '-files')
            # TODO: Remove this warning once snapshots are implemented
            logging.warning('GNS3 v1.0 does not currently support snapshots.'
                            ' The snapshots for this project will not be '
                            'saved')
            return
        else:
            topology_files_dir = os.path.join(output_dir, topology_name +
                                              '-files')

        # Prepare the directory structure
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Move the dynamips config files to the new topology folder
        if len(converter.configs) > 0:
            dynamips_config_dir = os.path.join(topology_files_dir, 'dynamips',
                                               'configs')
            os.makedirs(dynamips_config_dir)
            for config in converter.configs:
                old_config_file = os.path.join(old_topology_dir, config['old'])
                new_config_file = os.path.join(dynamips_config_dir,
                                               os.path.basename(config['new']))
                if os.path.isfile(old_config_file):
                    # Copy and rename the config
                    shutil.copy(old_config_file, new_config_file)
                else:
                    config_err = True
                    logging.error('Unable to find %s' % config['old'])

        # Move the image files to the new topology folder if applicable
        if len(converter.images) > 0:
            images_dir = os.path.join(output_dir, topology_name + '-files',
                                      'images')
            os.makedirs(images_dir)
            for image in converter.images:
                old_image_file = os.path.abspath(image)
                new_image_file = os.path.join(images_dir,
                                              os.path.basename(image))
                if os.path.isfile(os.path.abspath(old_image_file)):
                    shutil.copy(old_image_file, new_image_file)
                else:
                    image_err = True
                    logging.error('Unable to find %s' % old_image_file)

        # Create the vbox working directories if applicable
        vbox_max = json_topology.get_vboxes()
        if vbox_max is not None:
            for i in range(1, vbox_max + 1):
                vbox_dir = os.path.join(output_dir, topology_name + '-files',
                                        'vbox', 'vm-%s' % i)
                os.makedirs(vbox_dir)

        # Create the vbox working directories if applicable
        qemu_max = json_topology.get_qemus()
        if qemu_max is not None:
            for i in range(1, qemu_max + 1):
                qemu_dir = os.path.join(output_dir, topology_name + '-files',
                                        'qemu', 'vm-%s' % i)
                os.makedirs(qemu_dir)

        if config_err:
            logging.warning('Some router startup configurations could not be '
                            'found to be copied to the new topology')

        if image_err:
            logging.warning('Some images could not be found to be copied to '
                            'the new topology')

        filename = '%s.gns3' % topology_name
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as file:
            json.dump(json_topology.get_topology(), file, indent=4,
                      sort_keys=True)
            if not snapshot:
                print('Your topology has been converted and can found in:\n'
                      '     %s' % output_dir)
    except OSError as error:
        logging.error(error)


if __name__ == '__main__':
    main()
