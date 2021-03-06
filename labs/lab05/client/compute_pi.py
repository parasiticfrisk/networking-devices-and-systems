#!/usr/bin/env python3
#
# Author: August Frisk
# Course: CmpEt 269 - Spring 2018
# Assign: Lab 05
# File: compute_pi.py
#
# Description: Computes the value of Pi using the 'dartboard' algorithm — a
#              Monte Carlo method using many trials to estimate the area of a
#              quarter circle inside a unit square.
#
#              This code uses Dispy on OctaPi in standard form.
#
# Reference: Arndt & Haenel, "Pi - Unleashed", Springer-Verlag,
#            ISBN 978-3-540-66572-4, 2006,
#            English translation Catriona and David Lischka, pp. 39-41
#


# 'compute' is distributed to each node running 'dispynode'
def compute(s, n):
    import time, random

    inside = 0

    # set the random seed on the server from that passed by the client
    random.seed(s)

    # for all the points requested
    for i in range(n):
        # compute position of the point
        x = random.uniform(0.0, 1.0)
        y = random.uniform(0.0, 1.0)
        z = x * x + y * y
        if z <= 1.0:
            inside = inside + 1  # this point is inside the unit circle

    return (s, inside)


# main
if __name__ == "__main__":
    import dispy, random, argparse, resource

    resource.setrlimit(
        resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY)
    )
    resource.setrlimit(
        resource.RLIMIT_DATA, (resource.RLIM_INFINITY, resource.RLIM_INFINITY)
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "no_of_points", type=int, help="number of random points to include in each job"
    )
    parser.add_argument("no_of_jobs", type=int, help="number of jobs to run")
    args = parser.parse_args()

    no_of_points = args.no_of_points
    no_of_jobs = args.no_of_jobs
    server_nodes = "192.168.1.*"

    cluster = dispy.JobCluster(compute, nodes=server_nodes)
    print(
        (
            "submitting %i jobs of %i points each to %s"
            % (no_of_jobs, no_of_points, server_nodes)
        )
    )
    jobs = []
    for i in range(no_of_jobs):
        # schedule execution of 'compute' on a node (running 'dispynode')
        ran_seed = random.randint(
            0, 65535
        )  # define a random seed for each server using the client RNG
        job = cluster.submit(ran_seed, no_of_points)
        job.id = i  # associate an ID to the job
        jobs.append(job)

    total_inside = 0
    for job in jobs:
        ran_seed, inside = job()  # waits for job to finish and returns results

        total_inside += inside

        if job.id % 1000 == 0:
            print(
                ("executed job %s using %i with result %i" % (job.id, ran_seed, inside))
            )

    # calclate the estimated value of Pi
    total_no_of_points = no_of_points * no_of_jobs
    Pi = (4.0 * total_inside) / total_no_of_points
    print(
        ("value of Pi is estimated to be %f using %i points" % (Pi, total_no_of_points))
    )

    cluster.print_status()
