
#!/usr/bin/env python

# Copyright (c) 2014 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


from steelscript.commands.steel import BaseCommand

"""This program retrieves a list of valid columns for the current netprofiler.

Example:

 python netprofiler-columns.py dev-staging2.lab.nbttech.com -r traffic_summary --centricity hos

Column                                 Label                                  Id
app_name                               Application                            17
app_raw                                Raw app                                94
avg_bytes                              Avg Bytes/s                            33
avg_bytes_app                          Avg App Bytes/s                        504
avg_bytes_app_persecconn               Avg App Bytes/s per Conn               578
avg_bytes_persecconn                   Avg Bytes/s per Conn                   556
avg_bytes_rtx                          Avg Retrans Bytes/s                    391
avg_conns_active                       Avg Active Connections/s               532
avg_conns_new                          Avg New Connections/s

python netprofiler-columns.py -i 729,848,40,41,158,4,14,44,10,45,46,47,50,124,48,49,51,123,39 dev-staging2.lab.nbttech.com
Column                      Label                       Id

c2s_flags                   C2S_FLAGS                   50
c2s_total_bytes             Total Bits (cli -> srv)     46
c2s_total_pkts              Total Packets (cli -> srv)  47
cli_host_dns                Client                      14
cli_port                    Client Port                 44
cli_topo_dns                Topology (cli -> srv)       124
duration                    Duration                    158
end_time                    End Time                    41
flow_parts                  Row                         729
parent_id                   Parent FID                  39
protocol_name               Protocol                    4
s2c_flags                   S2C_FLAGS                   51
s2c_total_bytes             Total Bits (srv -> cli)     48
s2c_total_pkts              Total Packets (srv -> cli)  49
srv_host_dns                Server                      10
srv_port                    Server Port                 45
srv_topo_dns                Topology (srv -> cli)       123
start_time                  Start Time                  40
vxlan_name                  Virtual Network Tunnel      848
"""

from steelscript.netprofiler.core.app import NetProfilerApp
from steelscript.common.datautils import Formatter
import optparse


class Command(NetProfilerApp):
    help = 'List columns available for NetProfiler reports'

    def add_options(self, parser):

        group = optparse.OptionGroup(parser, "Report column information")
        group.add_option('--list-groupbys', default=False, action='store_true',
                         help='Show list of valid groupbys instead of columns')

        group.add_option('-c', '--centricity', dest='centricity', default=None,
                         help="centricity to query for")
        group.add_option('-r', '--realm', dest='realm', default=None,
                         help="realm to query for")
        group.add_option('-g', '--groupby', dest='groupby', default=None,
                         help="groupby to query for")
        group.add_option('-i', '--ids', dest='ids', default=None,
                         help="column id numbers to include in results")
        group.add_option('-f', '--filter',
                         help="filter columns on this string")
        parser.add_option_group(group)

        super(Command, self).add_options(parser)

    def print_columns(self, columns):
        keys = []
        values = []
        for c in columns:
            if (self.options.filter and
                    self.options.filter.lower() not in c.label.lower()):
                continue

            item = (c.key, c.label, c.id)
            if c.iskey:
                keys.append(item)
            else:
                values.append(item)

        Formatter.print_table(keys, ['Key Columns', 'Label', 'ID'])
        print ''
        Formatter.print_table(values, ['Value Columns', 'Label', 'ID'])

    def main(self):
        if self.options.list_groupbys:
            header = ["GroupBy", "Id"]
            data = [(k, v) for k, v in self.netprofiler.groupbys.iteritems()]
            data.sort()
            Formatter.print_table(data, header)
        else:
            if self.options.ids:
                columns = self.netprofiler.get_columns_by_ids(self.options.ids)
            else:
                o = self.options

                # find groupby looking in keys and values
                if o.groupby in self.netprofiler.groupbys:
                    groupby = self.netprofiler.groupbys[o.groupby]
                elif o.groupby in self.netprofiler.groupbys.values():
                    groupby = o.groupby
                else:
                    groupby = None

                args = {
                    'realms': [o.realm] if o.realm else None,
                    'centricities': [o.centricity] if o.centricity else None,
                    'groupbys': [groupby] if groupby else None,
                    }
                columns = self.netprofiler.search_columns(**args)

            columns.sort(key=lambda x: x.key)
            self.print_columns(columns)
