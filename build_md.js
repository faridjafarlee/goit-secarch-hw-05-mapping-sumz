// Генерує README.md з content.js: Markdown-версія ДЗ5 для швидкого перегляду.
const fs = require('fs'); const C = require('./content.js');
const esc = s => String(s).replace(/\|/g, '\\|');
const tbl = (h, rows) => ['| ' + h.join(' | ') + ' |', '|' + h.map(() => '---').join('|') + '|', ...rows.map(r => '| ' + r.map(esc).join(' | ') + ' |')].join('\n');
let md = `# ${C.title}\n\n` + tbl(['Поле', 'Значення'], C.meta) + '\n\n## Контекст\n\n' + C.context.join('\n\n') + '\n\n';
md += '## 1-2. Три загрози СУМЗ і їхні категорії STRIDE\n\n' + tbl(['№', 'Загроза', 'Компонент DFD', 'STRIDE', 'Звʼязок з ДЗ2 / ДЗ3'], C.overview) + '\n\n';
for (const t of C.threats) md += `### ${t.id}. ${t.title}\n\n` + tbl(['Поле', 'Опис'], [['STRIDE', t.stride], ['Компонент', t.component], ['Як реалізується', t.scenario], ['Чому важлива саме тут', t.why]]) + '\n\n';
md += '## 3. Техніки MITRE ATT&CK\n\n';
for (const t of C.threats) md += `### ${t.id}. ${t.title}\n\n` + tbl(['ID', 'Назва техніки', 'Тактика', 'Що це', 'Чому релевантна'], C.attack[t.id]) + '\n\n';
md += `> ${C.idNote}\n\n## 4. Контролі NIST SP 800-53 Rev. 5\n\n`;
for (const t of C.threats) md += `### ${t.id}. ${t.title}\n\n` + tbl(['Код', 'Назва контролю', 'Роль', 'Як допомагає в СУМЗ'], C.nist[t.id]) + `\n\nD3FEND (опційно): ${C.d3fend[t.id]}\n\n`;
md += '## 5. Розміщення контролів в архітектурі СУМЗ\n\n' + C.placementIntro + '\n\n![DFD СУМЗ з контролями](dfd_controls.png)\n\n' + tbl(['Контроль', 'Загр.', 'Рівень / компонент DFD', 'Реалізація', 'MVP', 'Ресурси'], C.placement) + '\n\n';
md += '### Що можна зробити в MVP і що потребує ресурсів\n\n' + C.mvp.map(t => '- ' + t).join('\n') + '\n\n## 6. Висновок\n\n' + tbl(['Питання', 'Відповідь'], C.conclusion) + '\n\n';
md += `## ${C.extra.title}\n\n${C.extra.intro}\n\n### Як змінюються загрози\n\n` + tbl(['STRIDE', 'Нова або змінена загроза', 'ATT&CK'], C.extra.threats) + '\n\n### Які контролі додати або посилити\n\n' + tbl(['Код', 'Назва', 'Що змінюється'], C.extra.controls) + '\n\n';
md += '## Зведена матриця трасування\n\n' + tbl(['Загроза', 'STRIDE', 'ATT&CK', 'NIST SP 800-53', 'Рівень', 'MVP'], C.trace) + '\n\n---\n\nЗбірка: спочатку `python3 draw_dfd_controls.py`, потім `NODE_PATH=<node_modules з docx> node build_docx.js`, потім `node build_md.js`. Файли для здачі: `ДЗ5_Джафарлі_Фарід.docx` (завантажити в Google Docs і відкрити доступ на перегляд) і `ДЗ5_Джафарлі_Фарід.zip`. Нічого не здано, подає сам студент.\n';
fs.writeFileSync('README.md', md); console.log('README.md', md.length);
