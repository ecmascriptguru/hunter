{% load static %}
# activator

Please follow the instructions carefully.

## Preparation

### Download Script
In order to reactivate a credential blocked by Google or LinkedIn, you need to download a python script. When you are ready to go, click [`here`]({% static 'tools/activator.zip' %}) to download now and extract a specific path and cd.
```shell
you@machine:script/path$
```

### Virtual Env Configuration
In order to execute the script, please prepare a specific virtuen env. Suppose that you've created a virtual env named **activator**. Then you will see the following prefix in your shell.
```shell
(activator)you@machine:script/path$
```

### Dependency Installation
Now, you are ready to install python packages.
```shell
pip install -r requirements.txt
```

## Reactivating Credential

### Open a browser with specific proxy configuration.
Now you are ready to start the reactivating process and just execute the following command.
```shell
python run.py
```
Then the script will ask you enter the proxy to be used in this activation thread. Please copy and paste the following proxy to the shell.
```
{{ proxy }}
```
When you press `Enter`, a selenium browser will be launched.

### Credential Configuration
Once the browser launched, you will be asked to enter credential email and password. The email is `{{ email }}` and password is `{{ password }}`. Git those to the script then the script will start activating google account.

### Activating Google Account
Almostly, you don't need to do anything here because this script does as much as needed automatically. But everything changes, so you might need to do it manually. For instance, google sometimes requires reCaptha then it's your turn to reactivate the google account for yourself. When you've asked to choose/give recovery info, then here it is.
```
Recovery Email: {{ recovery_email }}
Recovery Phone: {{ recovery_phone }}
```

When you think that the account was successfully unlocked, then press any ken in the shell to continue

### Activating LinkedIn Account
Of course this step was intended to reactivate the account automatically by itself. But linkedin might show you complex recaptcha problems. In that case the credential couldn't be solved automatically so please unlock the linkedin account manually by giving the access code got from email sent by linkedin. In case of image recaptcha, please investigate to unlock by giving answers to the recaptcha problems.

## Finalization
Once you think it can get into linkedin as well as google, it can be marked as **Active** by clikcing `Activated` button or you can retry.

> That's all and thank you for your attention!