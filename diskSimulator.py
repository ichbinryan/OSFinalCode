from pyeclib.ec_iface import ECDriver
import argparse
import timeit

parser = argparse.ArgumentParser(description='Disk encoding simulator.')
parser.add_argument('k', type=int, help='number of data disks')
parser.add_argument('m', type=int, help='number of coding disks')
parser.add_argument('ec_type', help='EC algorithm used')
parser.add_argument('filename', help='file to encode')

args = parser.parse_args()

ec_driver = ECDriver(k=args.k, m=args.m, ec_type=args.ec_type)

#word_size = 8

print("Data disks (k) = %d\nCoding disks (m) = %d" % (args.k, args.m))
#print("Word size = %d\n" %word_size)
print("ec_type = %s" % args.ec_type)
print("filename = %s" % args.filename)

file_dir = "./"+args.filename
frag_der = "./nodes"

f = open(file_dir)

m=0
#loop through file

start_time = timeit.default_timer()
end_time = 0
while True:
    j=0
    piece = f.read(1024*args.k*62)
    # also try 1024 * k * word_size * 4264
    if not piece:
        break
    #data_buffer[i] = piece

    for i in range(0, args.k):
        start_time = timeit.default_timer()
        fragments = ec_driver.encode(piece)
        end_time += timeit.default_timer() - start_time


    for fragment in fragments:
        with open("%s/%d/%s.%d.%d" % (frag_der, j, args.filename, j, m), "wb") as fp:
            fp.write(fragment)

        j += 1

    m += 1


print("Encoding time: %f seconds." % end_time)
