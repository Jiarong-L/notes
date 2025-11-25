

得到高质量的MAGs后，鉴定出所有的酶和代谢反应(KEGG/MetaCyc)，即得到GEMs(Genome-scale metabolic model)。可以使用自动化工具[carveme](https://carveme.readthedocs.io/en/latest/index.html)/modelSEED/KBase，它从物种完整的GEM (默认使用[BiGG Models](http://bigg.ucsd.edu/data_access)，包含物种中大量经过手动验证的高质量反应)中选取符合基因组注释信息（基础功能！）、培养基成分约束、合成辅因子/自身脂质的约束，并尽可能让模型变得简洁（最小化模型中的总反应数量）

得到GEMs（SBML格式 --> Edge/Path=Reactions,Node=Metabolites）后，即可开始 Flux Balance Analysis（FBA）。

Flux指代谢反应```A <-> B```在单位时间、单位细胞质量下的转化速率，```net = forward - reverse```。数值上，负数表示消耗、正数表示产出


## FBA 模拟示例

假设有一个大肠杆菌的GEM [iML1515](http://bigg.ucsd.edu/models/iML1515)，模拟它在葡萄糖基本培养基中的好氧生长，希望预测最生长速率

使用 [cobrapy](https://cobrapy.readthedocs.io/en/latest/building_model.html)，其中 ```model.objective``` 仅针对 Reactions，若希望优化某一代谢物，只能选取与其相关的 ```model.exchanges/.demands/``` 反应（e.g.代谢物在 ```rxn.metabolites``` 中）

反应分为 ```exchanges 细胞与外部环境之间的双向交换```，```demands 细胞内代谢物的消耗或需求```，```sinks 模型填充时临时提供代谢物(？)```

```py
import pandas as pd
import cobra
from cobra.util.solver import linear_reaction_coefficients
from cobra.flux_analysis import flux_variability_analysis

##  help(model) to see its attributes, like: .reactions .metabolites .genes
model = cobra.io.load_model('iML1515')      # if web fails, use .read_sbml_model('local.xml')  

## set _e intakes closed by default (-intake, +output) mmol/gDW/h
for reaction in model.exchanges:
    if reaction.id not in 
    reaction.bounds = (0, 1000)

## set medium bounds 
medium = { rxn_id:(-1000, 1000) for rxn_id in ['EX_nh4_e','EX_pi_e','EX_so4_e','EX_k_e','EX_na_e','EX_fe2_e','EX_mg2_e','EX_cl_e','EX_ca2_e','EX_cobalt2_e','EX_cu2_e','EX_mn2_e','EX_zn2_e','EX_mobd_e']}
medium.update({
    'EX_glc__D_e': (-10, 1000),    # Glucose
    'EX_o2_e': (-20, 1000),        # Oxygen, aerobic
})

for rxn_id, bounds in medium.items():
    try:
        reaction = model.reactions.get_by_id(rxn_id)
        reaction.bounds = bounds
    except:
        print(f"reaction {rxn_id} not in the model")


## run FBA 
model.objective = {                                         # print(linear_reaction_coefficients(model)) 
    model.reactions.BIOMASS_Ec_iML1515_core_75p37M: 1.0,    # default obj
    model.reactions.EX_ac_e: 0.5 
}
assert model.reactions.get_by_id("BIOMASS_Ec_iML1515_core_75p37M").upper_bound == 1000
assert model.reactions.get_by_id("EX_ac_e").upper_bound == 1000

solution = model.optimize('maximize')  ##  {None, 'maximize' 'minimize'}
print(f"{solution.fluxes['EX_glc__D_e']:.4f} mmol/gDW/h")  ## see each reactions
print(model.summary())  ## fva=0.95
flux_variability_analysis(model, model.reactions[:10], loopless=True)  ## FVA -- finds the ranges of each metabolic flux 
```


总之，设计不同的优化目标（e.g. 多产物合成=sum，碳利用效率=生长-葡萄糖消耗，...），计算理论得率，权衡不同通路的重要性/模拟不同环境下的代谢结果/模拟基因敲除后的结果（对包含这个基因的反应/这个基因```.knock_out()```，cobrapy提供单次敲除1-2个基因的批量模拟```single_gene_deletion(model)```），或筛查添加哪些反应能使模型变得可行 ```gapfill(failed_model, pan_model, demand_reactions=False, iterations=4)```

如果最优解的一致性不佳，可能存在 blocked reactions，用 ```cobra.flux_analysis.find_blocked_reactions(model)``` 查看

此外，如果认为一些通量异常的高、或FVA范围异常大，需要考虑是否是loop造成的（对比Loopless模式的结果）

如果有代谢组数据（一般是多个物种但暂且假设在一个整体循环内），可以根据其比例设置相关反应的通量约束bounds，或许也可以写一个壳子来优化这些约束（e.g.gradient）/其它Graph模拟。FBA模型本质上只是在拟合不同通路的权重，只能依据生产/消耗反应的通量来间接影响代谢物的预测浓度、模型中最多设置 ```model.add_boundary(model.metabolites.xx_c, type='demand')```

除了最优解，flux sampling ```s = sample(model, 100)``` 可以探索（符合约束条件的）稳态下所有可能的Flux分布


