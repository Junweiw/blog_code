const GJJ_CAP = 44265;

const TAX_BRACKETS = [
  { limit: 36000, rate: 0.03, quick: 0 },
  { limit: 144000, rate: 0.10, quick: 2520 },
  { limit: 300000, rate: 0.20, quick: 16920 },
  { limit: 420000, rate: 0.25, quick: 31920 },
  { limit: 660000, rate: 0.30, quick: 52920 },
  { limit: 960000, rate: 0.35, quick: 85920 },
  { limit: Infinity, rate: 0.45, quick: 181920 },
];

function formatMoney(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  return `${Math.round(value).toLocaleString('zh-CN')} 元`;
}

function formatPercent(value) {
  return `${Math.round(value * 100)}%`;
}

function shenzhenSocialInsurancePersonal(salary) {
  const pensionBase = Math.min(Math.max(salary, 4775), 27549);
  const medicalBase = Math.min(Math.max(salary, 6733), 33666);
  const unemploymentBase = Math.min(Math.max(salary, 2360), 27549);
  return pensionBase * 0.08 + medicalBase * 0.02 + unemploymentBase * 0.002;
}

function gjjPersonal(salary, rate) {
  const base = Math.min(salary, GJJ_CAP);
  return base * rate;
}

function calcTaxAnnual(monthlyTaxable) {
  const annual = monthlyTaxable * 12;
  if (annual <= 0) return { tax: 0, rate: 0 };

  for (const bracket of TAX_BRACKETS) {
    if (annual <= bracket.limit) {
      return { tax: annual * bracket.rate - bracket.quick, rate: bracket.rate };
    }
  }
  return { tax: 0, rate: 0 };
}

function getSpecialDeduction() {
  let total = 0;
  document.querySelectorAll('.deductions input[type="checkbox"]:checked').forEach((el) => {
    total += Number(el.dataset.amount);
  });
  total += Number(document.getElementById('customDeduction').value) || 0;
  return total;
}

function analyzeScenario(salary, currentRate, targetRate, specialDeduction) {
  const si = shenzhenSocialInsurancePersonal(salary);
  const gjjCurrent = gjjPersonal(salary, currentRate);
  const gjjTarget = gjjPersonal(salary, targetRate);
  const deltaGjj = Math.max(gjjTarget - gjjCurrent, 0);

  const taxableCurrent = salary - 5000 - si - gjjCurrent - specialDeduction;
  const taxableTarget = salary - 5000 - si - gjjTarget - specialDeduction;

  const taxCurrent = calcTaxAnnual(taxableCurrent);
  const taxTarget = calcTaxAnnual(taxableTarget);

  const annualTaxSave = Math.max(taxCurrent.tax - taxTarget.tax, 0);
  const monthlyTaxSave = annualTaxSave / 12;
  const monthlyCashCost = deltaGjj - monthlyTaxSave;
  const loanBoost1y = deltaGjj * 12 * 16;
  const loanBoost3y = deltaGjj * 36 * 16;

  return {
    si,
    gjjBase: Math.min(salary, GJJ_CAP),
    gjjCurrent,
    gjjTarget,
    deltaGjj,
    taxableCurrent: Math.max(taxableCurrent, 0),
    taxableTarget: Math.max(taxableTarget, 0),
    marginalRate: taxTarget.rate,
    annualTaxCurrent: taxCurrent.tax,
    annualTaxTarget: taxTarget.tax,
    annualTaxSave,
    monthlyTaxSave,
    monthlyCashCost,
    loanBoost1y,
    loanBoost3y,
  };
}

function getRecommendation(result, inputs) {
  const { currentRate, targetRate, homePlan, cashTolerance } = inputs;
  const {
    deltaGjj,
    marginalRate,
    annualTaxSave,
    monthlyCashCost,
    loanBoost1y,
  } = result;

  if (currentRate >= 0.12) {
    return {
      level: 'neutral',
      icon: 'ℹ️',
      title: '已达最高比例',
      detail: '个人缴存比例已是 12%，本公积金年度内无法再通过提高个人比例获得额外节税或提额。',
    };
  }

  if (targetRate <= currentRate) {
    return {
      level: 'neutral',
      icon: 'ℹ️',
      title: '目标比例未高于当前',
      detail: '请选择高于当前个人比例的目标比例后再计算。',
    };
  }

  if (deltaGjj === 0) {
    return {
      level: 'neutral',
      icon: 'ℹ️',
      title: '无变化',
      detail: '当前与目标比例相同，无需调整。',
    };
  }

  const cashOk = monthlyCashCost <= cashTolerance;
  const hasHomePlan = homePlan !== 'none';
  const hasRepay = homePlan === 'repay';

  if (annualTaxSave <= 0 && !hasHomePlan) {
    return {
      level: 'no',
      icon: '❌',
      title: '不建议提升',
      detail: '当前几乎无个税，提升比例无法节税，且会减少到手工资。若无购房计划，建议维持原比例。',
    };
  }

  if (annualTaxSave <= 0 && hasHomePlan) {
    if (!cashOk) {
      return {
        level: 'caution',
        icon: '⚠️',
        title: '谨慎提升',
        detail: `虽无节税收益，但 1 年后贷款额度可增加约 ${formatMoney(loanBoost1y)}。不过月到手减少 ${formatMoney(monthlyCashCost)}，超出你的承受范围。`,
      };
    }
    return {
      level: 'caution',
      icon: '⚠️',
      title: '可考虑提升（为购房攒余额）',
      detail: `无节税收益，但 1 年后贷款额度可增加约 ${formatMoney(loanBoost1y)}。若现金流允许，可为目标比例 ${formatPercent(targetRate)}。`,
    };
  }

  if (hasRepay && cashOk) {
    return {
      level: 'yes',
      icon: '✅',
      title: '建议提升',
      detail: `你已有公积金贷款并冲还贷，多缴部分可直接抵扣月供。年节税约 ${formatMoney(annualTaxSave)}，实际现金压力更小。`,
    };
  }

  if (marginalRate >= 0.20 && cashOk && hasHomePlan) {
    return {
      level: 'strong',
      icon: '✅',
      title: '强烈建议提至目标比例',
      detail: `边际税率 ${formatPercent(marginalRate)}，年节税约 ${formatMoney(annualTaxSave)}，1 年后贷款额度增加约 ${formatMoney(loanBoost1y)}，节税与提额双重收益明显。`,
    };
  }

  if (marginalRate >= 0.10 && cashOk) {
    return {
      level: 'yes',
      icon: '✅',
      title: hasHomePlan ? '建议提升' : '建议提升（节税为主）',
      detail: `边际税率 ${formatPercent(marginalRate)}，年节税约 ${formatMoney(annualTaxSave)}。${hasHomePlan ? `1 年后贷款额度增加约 ${formatMoney(loanBoost1y)}。` : '暂无购房计划，主要收益来自节税。'}`,
    };
  }

  if (marginalRate >= 0.03 && hasHomePlan && cashOk) {
    return {
      level: 'caution',
      icon: '⚠️',
      title: '可考虑部分提升',
      detail: `边际税率较低（${formatPercent(marginalRate)}），节税有限。若有购房需求，可提至 8%–10% 折中，兼顾余额积累与现金流。`,
    };
  }

  if (!cashOk) {
    return {
      level: 'caution',
      icon: '⚠️',
      title: '节税有收益，但现金流偏紧',
      detail: `年节税约 ${formatMoney(annualTaxSave)}，但月到手将减少 ${formatMoney(monthlyCashCost)}，超出你设定的 ${formatMoney(cashTolerance)} 承受上限。可考虑较低目标比例。`,
    };
  }

  return {
    level: 'caution',
    icon: '⚠️',
    title: '谨慎提升',
    detail: '节税收益有限，且暂无明确购房计划。建议维持原比例，或仅小幅提升。',
  };
}

function shortRecommendation(result, inputs) {
  const rec = getRecommendation(result, inputs);
  if (rec.level === 'strong' || rec.level === 'yes') return '建议';
  if (rec.level === 'no') return '不建议';
  return '谨慎';
}

function renderComparison(result) {
  const rows = [
    ['公积金缴存基数', formatMoney(result.gjjBase), formatMoney(result.gjjBase), '—'],
    ['公积金个人缴存', formatMoney(result.gjjCurrent), formatMoney(result.gjjTarget), `+${formatMoney(result.deltaGjj)}`],
    ['月应纳税所得额', formatMoney(result.taxableCurrent), formatMoney(result.taxableTarget), `−${formatMoney(result.taxableCurrent - result.taxableTarget)}`],
    ['年个税', formatMoney(result.annualTaxCurrent), formatMoney(result.annualTaxTarget), `−${formatMoney(result.annualTaxSave)}`],
    ['1 年账户余额（个人）', formatMoney(result.gjjCurrent * 12), formatMoney(result.gjjTarget * 12), `+${formatMoney(result.deltaGjj * 12)}`],
    ['1 年贷款额度提升', '—', '—', `+${formatMoney(result.loanBoost1y)}`],
    ['3 年贷款额度提升', '—', '—', `+${formatMoney(result.loanBoost3y)}`],
  ];

  document.getElementById('compareBody').innerHTML = rows
    .map(([label, before, after, change]) => `
      <tr>
        <td>${label}</td>
        <td>${before}</td>
        <td>${after}</td>
        <td class="${change.startsWith('+') ? 'positive' : change.startsWith('−') ? 'negative' : ''}">${change}</td>
      </tr>
    `)
    .join('');
}

function renderScenarios(salary, currentRate, specialDeduction, inputs) {
  const rates = [0.08, 0.09, 0.10, 0.11, 0.12].filter((r) => r > currentRate);
  const tbody = document.getElementById('scenarioBody');

  if (rates.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6">当前比例已达或超过 12%，无可对比方案。</td></tr>';
    return;
  }

  tbody.innerHTML = rates.map((rate) => {
    const scenario = analyzeScenario(salary, currentRate, rate, specialDeduction);
    const scenarioInputs = { ...inputs, targetRate: rate };
    const rec = shortRecommendation(scenario, scenarioInputs);
    const recClass = rec === '建议' ? 'positive' : rec === '不建议' ? 'negative' : '';
    return `
      <tr>
        <td>${formatPercent(rate)}</td>
        <td>+${formatMoney(scenario.deltaGjj)}</td>
        <td>${formatMoney(scenario.monthlyTaxSave)}</td>
        <td>${formatMoney(scenario.monthlyCashCost)}</td>
        <td>+${formatMoney(scenario.loanBoost1y)}</td>
        <td class="${recClass}">${rec}</td>
      </tr>
    `;
  }).join('');
}

function renderResults() {
  const salary = Number(document.getElementById('salary').value);
  const currentRate = Number(document.getElementById('currentRate').value) / 100;
  const targetRate = Number(document.getElementById('targetRate').value) / 100;
  const employerRate = Number(document.getElementById('employerRate').value) / 100;
  const homePlan = document.getElementById('homePlan').value;
  const cashTolerance = Number(document.getElementById('cashTolerance').value) || 0;
  const specialDeduction = getSpecialDeduction();

  if (!salary || salary < 2360) {
    alert('请输入有效的税前月薪（不低于 2360 元）。');
    return;
  }

  const result = analyzeScenario(salary, currentRate, targetRate, specialDeduction);
  const inputs = { currentRate, targetRate, employerRate, homePlan, cashTolerance };
  const rec = getRecommendation(result, inputs);

  const recEl = document.getElementById('recommendation');
  recEl.className = `recommendation rec-${rec.level}`;

  document.getElementById('recIcon').textContent = rec.icon;
  document.getElementById('recTitle').textContent = rec.title;
  document.getElementById('recDetail').textContent = rec.detail;

  document.getElementById('metricDelta').textContent = result.deltaGjj > 0 ? `+${formatMoney(result.deltaGjj)}` : '—';
  document.getElementById('metricRate').textContent = formatPercent(result.marginalRate);
  document.getElementById('metricTaxSave').textContent = formatMoney(result.monthlyTaxSave);
  document.getElementById('metricCashCost').textContent = formatMoney(result.monthlyCashCost);
  document.getElementById('metricAnnualTax').textContent = formatMoney(result.annualTaxSave);
  document.getElementById('metricLoan1y').textContent = result.loanBoost1y > 0 ? `+${formatMoney(result.loanBoost1y)}` : '—';

  renderComparison(result);
  renderScenarios(salary, currentRate, specialDeduction, inputs);

  document.getElementById('resultsPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function syncTargetOptions() {
  const current = Number(document.getElementById('currentRate').value);
  const targetSelect = document.getElementById('targetRate');
  Array.from(targetSelect.options).forEach((opt) => {
    opt.disabled = Number(opt.value) <= current;
  });
  if (Number(targetSelect.value) <= current) {
    const next = Array.from(targetSelect.options).find((opt) => Number(opt.value) > current);
    if (next) targetSelect.value = next.value;
  }
}

document.getElementById('calculateBtn').addEventListener('click', renderResults);
document.getElementById('currentRate').addEventListener('change', syncTargetOptions);

document.querySelectorAll('input, select').forEach((el) => {
  el.addEventListener('change', () => {
    if (document.getElementById('recTitle').textContent !== '填写信息后点击计算') {
      renderResults();
    }
  });
});

syncTargetOptions();
renderResults();
