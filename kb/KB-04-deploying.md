# KB-04 Deploying your app

Click **Deploy** in the top bar. Buildbox builds your app and publishes it at
`<project-name>.bbx.example`. The first deploy usually takes 1 to 3 minutes; later deploys are
faster.

- Each deploy is a snapshot. Changing the project afterwards does not change the live site until
  you deploy again.
- **Deploy history** lists every deploy with its build log. "Roll back" makes an older deploy live
  again in a few seconds.
- The live app uses the environment variables marked **Production** (see KB-08). The preview uses
  the ones marked **Preview**.
- Apps on the Free plan sleep after 24 hours without visits and wake on the next request (a few
  seconds). Paid plans do not sleep.
- If a deploy fails, see KB-05.
