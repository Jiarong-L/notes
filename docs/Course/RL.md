<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global' 
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>


<style>
img{
    width: 60%;
}
</style>


参考：[EasyRL - 蘑菇书](https://datawhalechina.github.io/easy-rl/)，CS285旧笔记（见文件夹）

练习工具：[Gymnasium](https://gymnasium.org.cn/introduction/basic_usage/) 为一些常见的强化学习项目提供环境反馈


## 符号表

at timestep *t*  

$s_t$ - state     
$o_t$ - observation   
$a_t$ - action   
$\pi_\theta(a_t|o_t)$ - policy (partially observed)  
$\pi_\theta(a_t|s_t)$ - policy (fully observed)      
$\tau$ - Trajectory，试验得到的一系列($s_t$,$a_t$)组合  
$H_t$ - History，试验得到的一系列($s_t$,$a_t$,$r_t$)组合


## 基本知识

强化学习（Reinforcement Learning）的训练目标是：让智能体(Agent)的行为在不确定的环境中最大化奖励（Reward），其困难在于奖励的获取有延迟 / 权衡探索与利用（牺牲一部分短期奖励）

行为(action)可以是离散的（上下左右）也可以是连续的（分子某个亚基左旋多少度）

------------------------------------

一个RL训练样本是一个试验的历史轨迹($\tau$)，是一组时间序列，这有别于普通的监督学习（iid）

在一个试验(Trial)/一个回合(Episode)中，每一步$t$运行一次Agent（依照策略进行一次动作、Env返回新状态），直到游戏结束/超出预定步数

------------------------------------

**Agent 的组成 (at $s_t$)**

- Policy：依据当前状态选取动作
    - 随机/概率分布 $\pi(a|s)$ 即 $p(a_t = a | s_t = s)$
    - 确定/最优 $\mathop{\arg\min}\limits_{a} \pi(a|s)$ 

- Value Function：对未来累计奖励 $G_t = \sum\limits_{k=0}^{\infty} \gamma^{k} r_{t+k+1}$ 的预测
    - $V_{\pi}(s) = E_{\pi}[G_t | s_t = s] = \sum\limits_{a} Q_{\pi}(s,a)$
    - $Q_{\pi}(s,a) = E_{\pi}[G_t | s_t = s, a_t = a]$

- Model：施加选定的动作后，返回新状态 $s'$、奖励
    - 状态转移概率 $p_{ss'}^{a} = p(s_{t+1} = s' | s_t=s, a_t=a)$
    - 奖励 $R(s,a) = E[r_{t+1} | s_t=s, a_t=a ]$

Model-based 需要对环境建模、以预测反馈（e.g.一些游戏空间），但更多深度学习的情况是 Model-free、即直接从真实环境中获取反馈（e.g.自动驾驶上路训练），可能会有一些采样的问题（采样了s1路线的反馈，但模型跑在未知的s2路线上）

------------------------------------

Value-based Agent 会评估每一对(状态-动作)的价值，选择能带来最高价值的动作；间接获得**确定/最优**的策略，适合离散小空间中的穷举，例如：Q-Learning: $\pi(s) = argmax_a Q(s, a)$）

Policy-based Agent 直接学习策略的**概率分布** $\pi_{\theta}(a|s)$，可以借助价值方程训练策略分布的参数 $\theta$, 以最大化期望总回报，例如：Actor-Critic方法中，Actor根据策略概率抽选动作，Critic评估价值

------------------------------------









