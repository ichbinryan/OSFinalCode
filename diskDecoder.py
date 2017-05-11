from pyeclib.ec_iface import ECDriver
import argparse
import timeit
import os, os.path

parser = argparse.ArgumentParser(description='Disk encoding simulator.')
parser.add_argument('k', type=int, help='number of data disks')
parser.add_argument('m', type=int, help='number of coding disks')
parser.add_argument('ec_type', help='EC algorithm used')
parser.add_argument('filename', help='file to decode')
parser.add_argument('new_file', help='name of file to encode')
#parser.add_argument('Disk-path', help='directory path to disk array that contains our fragments')

args = parser.parse_args()

ec_driver = ECDriver(k=args.k, m=args.m, ec_type=args.ec_type)

k = args.k
m = args.m
ec_type = args.ec_type

new_file = open('./Client/%s' % args.new_file, 'wb+')

print("Data disks (k) = %d\nCoding disks (m) = %d" % (args.k, args.m))
#print("Word size = %d\n" % args.word_size)
print("ec_type = %s" % args.ec_type)
print("filename = %s" % args.filename)

#find directory size
num_stripes = 0


num_stripes = len([name for name in os.listdir('./nodes/0/')])

print("Number of fragments in single disk: %d" % num_stripes)

k = 0

#for i in range(0, k + m, 1):

start_time = 0
end_time = 0

downed_nodes = []

for i in range(0, num_stripes, 1):
    frags = []
    for j in range(args.m+args.k):
        try:
            f = open("./nodes/%d/%s.%d.%d" % (j, args.filename, j, i), 'rb')
            #print j
            frags.append(f.read())
        except IOError:
            if j not in downed_nodes:
                print("Logging data loss at node %d, notify name_node of downed node" % j)
                downed_nodes.append(j)

    start_time = timeit.default_timer()

    dec_chunk = ec_driver.decode(frags)

    end_time += timeit.default_timer()-start_time

    new_file.write(dec_chunk)

print("Decoding time: %f" % end_time)
