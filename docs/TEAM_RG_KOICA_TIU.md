# KOICA-TIU students: deploy into your team resource group

The walkthrough's fast path normally creates its own resource group
(`rg-cvbot-<suffix>`). KOICA-TIU hackathon students **cannot** create
subscription-level resource groups — operations grants each team
**Contributor on a pre-provisioned team resource group** instead
(e.g. `rg-koicatiu-team01`). Deploy into that group rather than creating one.

## How

Set `RESOURCE_GROUP` to your team RG before deploying. The scripts then use it
as-is and skip `az group create`:

```bash
export RESOURCE_GROUP=rg-koicatiu-team01   # your team's RG (ask your tutor)
export SUFFIX=cvbot01                      # still needed: names the OpenAI/ACR/app resources
export LOCATION=koreacentral

bash scripts/deploy_career_cv_aca.sh
```

Everything else (Azure OpenAI, ACR, Container App) is created **inside** your
team RG, and you have Contributor there, so it works without any
subscription-level rights.

For the manual walkthrough, do the same: `RG=rg-koicatiu-team01` and **skip the
`az group create` step** (Step 3b) — the group already exists.

## Teardown — important

Your team RG is **shared by your whole team**, so do **NOT** run
`az group delete` (that would wipe your teammates' work). Tear down only the
resources you created:

```bash
bash scripts/stop_career_cv_aca.sh     # stop the public URL (keeps resources)
# or remove just your app's resources by name, e.g.:
az containerapp delete --name "ca-cvbot-$SUFFIX" --resource-group "$RESOURCE_GROUP" --yes
```

Use a **unique `SUFFIX` per person/run** so teammates' resources don't collide
inside the shared team RG.

## Personal Azure trial

If you're using a personal free Azure trial instead, leave `RESOURCE_GROUP`
unset — the scripts create and (with the delete script) remove
`rg-cvbot-<suffix>` for you, exactly as the walkthrough describes.
