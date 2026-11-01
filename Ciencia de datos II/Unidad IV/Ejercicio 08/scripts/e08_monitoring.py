import json
from pathlib import Path
import yaml
from inf8239_u04.data import features, load_data, temporal_split
from inf8239_u04.governance import load_config
from inf8239_u04.mitigation import fit_exponentiated_gradient
from inf8239_u04.model import build_model
from inf8239_u04.monitoring import alerts, drift_table, monthly_report
from inf8239_u04.pipeline import run
cfg=load_config(); mon=yaml.safe_load(Path("configs/monitoring.yml").read_text(encoding="utf-8"))
df=load_data(); train,_=temporal_split(df); result=run(df,cfg["gates"])
monthly=monthly_report(result["test"],result["pred"],mon["min_support"])
drift=drift_table(train,result["test"],list(features(train).columns))
found=alerts(monthly,drift,mon)
# Same monthly view for the version recommended for the pilot (E07: ExponentiatedGradient, recall parity).
eg=fit_exponentiated_gradient(build_model("logistic"),features(train),train.target,train.protected_group)
monthly_eg=monthly_report(result["test"],eg(features(result["test"])),mon["min_support"]); found_eg=alerts(monthly_eg,drift,mon)
out=Path("reports/e08"); out.mkdir(parents=True,exist_ok=True)
monthly.round(4).to_csv(out/"monitoring_by_month.csv",index=False); drift.round(4).to_csv(out/"drift_psi.csv",index=False); found.to_csv(out/"monitoring_alerts.csv",index=False)
monthly_eg.round(4).to_csv(out/"monitoring_by_month_expgrad.csv",index=False); found_eg.to_csv(out/"monitoring_alerts_expgrad.csv",index=False)
summary={"reference":"train (hasta el corte temporal)","months":monthly.month.tolist(),"max_psi":round(float(drift.psi.max()),4),
         "alerts_by_level":found.level.value_counts().to_dict(),"alerts_by_level_expgrad":found_eg.level.value_counts().to_dict()}
(out/"monitoring_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
print(monthly.round(3).to_string(index=False)); print(drift.round(3).to_string(index=False)); print(found.to_string(index=False))
print("ExponentiatedGradient (versión del piloto)"); print(monthly_eg.round(3).to_string(index=False)); print(found_eg.to_string(index=False))
