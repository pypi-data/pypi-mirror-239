from core import *

os.chdir(manager_config.work_dir)
from mechanism.ipr_model.ipr_model import *

# %% 不同井型IPR测试

Pr_avg = 50  # 地层压力 MPa
Pb = 40  # 泡点压力 MPa

qo_test = 10000  # 测试点产量 sm3/d
Pwf_test = 5  # 测试点压力 MPa

FE = 1 - 0.2  # 流动效率 井的理想生产压差与实际生产压差的比 0.5~1.5
fw = 0.5  # 含水率 0.1 小数-%
Pwf = np.linspace(0, Pr_avg, num=100)

qo = f_IPR_vertical(qo_test, Pwf_test, Pwf, Pr_avg, Pb, fw, FE=1)

plt.figure()
plt.plot(qo, Pwf)
plt.xlabel('产量 sm3/d')
plt.ylabel('井底压力 MPa')
plt.xlim(0)
plt.ylim(0)
# plt.legend()
plt.grid()
plt.tight_layout()

plt.show()
