# Zato deployment with a blue green release strategy

Please read [this](https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html) for more info on what blue-green deployments are about and how they work etc and [this](zato.io) for more info on zato

At the time of making this, the latest zato release is V2.0.8. Which in my opinion is very buggy for my use case. So in the examples you will see that I use V3(from source) which is not yet released.

What you can create with this:
- A blue environment cluster
- A green environment cluster
- A web admin to manage both of the clusters

These are the resources I used. Where I work, we are big fans of AWS and their products, so I relied on them for all my needs. These are the services I used

- EC2 instances (1 instance for each zato component) (Inside elastic beanstalk)
- RDS for the ODB (Only one was needed)
- Redis in elasticache(I had one instance per environment.)

### How to deploy this in AWS.

Start by getting your resources ready in AWS (RDS and elasticache) as well as configure all the security groups.

Assuming this is all already configured and you're at the stage where you are about to deploy zato.

Update the `ENV` variables in the docker files to point to your new resources then zip the entire folder and launch your new environment. It will take some time to complete because we are installing zato from source. 

I used a small server for the webadmin(1cpu core and 500mb ram). In order to avoid memory issues while installing, I created a swap file

```
sudo dd if=/dev/zero of=/swapfile bs=1024 count=524288
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```
This allowed for some more memory availabilty which helped the install a lot!

After all your components have installed and are up and running. You need to keep track of the URLS provided by AWS (If you used elastic beanstalk) otherwise the public ips as you will need these all shortly.

Login to the web admin interface and head over to the `clusters` view. Once there, both your load balancers should report offline. Edit the blue cluster and replace the IP with the ip of the instance. Do the same with the green cluster. Now the clusters should be online and reporting everything fine. Go to each cluster and click `servers` and add the appropriate servers to each cluster. Once done, zato will tell you that `all servers are down`. Go to the `load-balancer` config in the webadmin for each cluster and update the ports of the servers (server1 is 17011, server2 is 17012). After this you should have a perfectly deployed zato environment that is ready for blue-green releases.

The nice part of this is that services in your green env are completly isolated from your blue env.

### How to use this in production.
So assuming you have deployed all of these instances in production and your environment is all set up the way to get blue green deployments down is super easy!

In the webadmin, under services(The place you upload all your code). Add all your services and configure your endpoints for these services. If you already have live services that consumers and vendoes are using, then this part is where it gets cool! You have two clusters(blue and green) and green is currently the production cluster. Now you are ready to take up some changes to services and even added some new ones. You will first add these services to the blue cluster(Staging) and test them and ensure you're ready. Once everything is good, the only thing you need to do is go live. All you is swap environment URLs in elastic beanstalk. (blue cluster with green cluster). This will shift the staging cluster into staging and revert the production cluster to staging. This update will leave no downtime whatsoever and will also allow for you to  revert your changes if needed by swapping the URLs again. (How cool is that). After some time you need to update the staging environment to catch up to what is in production. It is important that staging is always up to date or ahead of production for this to work well!


