// Збирає «ДЗ5_Джафарлі_Фарід.docx» з content.js і dfd_controls.png (docx-js).
// Запуск: NODE_PATH=<node_modules з docx> node build_docx.js
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType,
  ImageRun, AlignmentType, LevelFormat, BorderStyle, PageBreak } = require('docx');
const C = require('./content.js');

const FONT = 'Arial', W = 9638; // A4 мінус поля по 2 см
const border = { style: BorderStyle.SINGLE, size: 4, color: 'B8BEC9' };
const borders = { top: border, bottom: border, left: border, right: border };
const p = (text, o = {}) => new Paragraph({ spacing: { after: 120 }, ...o, children: [new TextRun({ text, font: FONT, size: 21, ...(o.run || {}) })] });
const h = (text, level) => new Paragraph({ heading: level, spacing: { before: 240, after: 120 }, children: [new TextRun({ text, font: FONT })] });
const bullet = t => new Paragraph({ numbering: { reference: 'bullets', level: 0 }, spacing: { after: 60 }, children: [new TextRun({ text: t, font: FONT, size: 21 })] });
const cell = (text, w, { head = false, bold = false, fill, size = 17 } = {}) => new TableCell({
  borders, width: { size: w, type: WidthType.DXA }, margins: { top: 60, bottom: 60, left: 90, right: 90 },
  shading: (head || fill) ? { fill: fill || 'E8EDF7', type: ShadingType.CLEAR, color: 'auto' } : undefined,
  children: [new Paragraph({ children: [new TextRun({ text, font: FONT, size, bold: head || bold })] })],
});
const table = (widths, header, rows, o = {}) => new Table({
  width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
  rows: [new TableRow({ tableHeader: true, children: header.map((t, i) => cell(t, widths[i], { head: true, size: o.size || 17 })) }),
    ...rows.map(r => new TableRow({ children: r.map((t, i) => cell(t, widths[i], { size: o.size || 17 })) }))],
});
const kv = (pairs, fill, kw = 2100) => new Table({ // «картка»: поле → значення; жирний лише перший рядок (заголовок картки)
  width: { size: W, type: WidthType.DXA }, columnWidths: [kw, W - kw],
  rows: pairs.map(([k, v], i) => new TableRow({ children: [
    cell(k, kw, { bold: i === 0, fill: i === 0 ? fill : 'F4F6FA', size: 18 }),
    cell(v, W - kw, { size: 18, fill: i === 0 ? fill : undefined, bold: i === 0 }),
  ] })),
});
const gap = () => new Paragraph({ spacing: { before: 120, after: 60 }, children: [] });
const FILL = { 'Загроза 1': 'E0E9FB', 'Загроза 2': 'FDEBDD', 'Загроза 3': 'EEE6FB' };

const b = [];
b.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: C.title, font: FONT, size: 34, bold: true })] }));
b.push(table([2000, W - 2000], ['Поле', 'Значення'], C.meta, { size: 18 }));
b.push(h('Контекст', HeadingLevel.HEADING_1)); C.context.forEach(t => b.push(p(t)));

b.push(h('1-2. Три загрози СУМЗ і їхні категорії STRIDE', HeadingLevel.HEADING_1));
b.push(table([500, 2950, 2500, 850, 2838], ['№', 'Загроза', 'Компонент DFD', 'STRIDE', 'Звʼязок з ДЗ2 / ДЗ3'], C.overview));
for (const t of C.threats) {
  b.push(gap());
  b.push(kv([[t.id + ' · ' + t.stride, t.title], ['Компонент', t.component], ['Як реалізується', t.scenario], ['Чому важлива саме тут', t.why]], FILL[t.id]));
}

b.push(new Paragraph({ children: [new PageBreak()] }));
b.push(h('3. Техніки MITRE ATT&CK', HeadingLevel.HEADING_1));
b.push(p('Для кожної загрози наведено ланцюг технік ATT&CK Enterprise, якими її реалізує атакувальник. Перша техніка в таблиці є точкою входу, наступні показують, як атака доходить до шкоди.'));
for (const t of C.threats) {
  b.push(h(t.id + '. ' + t.title, HeadingLevel.HEADING_2));
  b.push(table([1150, 2000, 1250, 2500, 2738], ['ID', 'Назва техніки', 'Тактика', 'Що це (своїми словами)', 'Чому релевантна загрозі'], C.attack[t.id]));
}
b.push(p(C.idNote, { spacing: { before: 160, after: 120 }, run: { italics: true, size: 18, color: '4B5563' } }));

b.push(h('4. Контролі NIST SP 800-53 Rev. 5', HeadingLevel.HEADING_1));
b.push(p('Контролі я брав з каталогу NIST SP 800-53 Rev. 5 і звіряв з мапуванням ATT&CK → NIST у CTID Mappings Explorer. Для кожного вказано роль: запобігає атаці, виявляє її або зменшує наслідки. Так видно, що кожну загрозу закривають кілька контролів з різних боків.'));
for (const t of C.threats) {
  b.push(h(t.id + '. ' + t.title, HeadingLevel.HEADING_2));
  b.push(table([1150, 2400, 1300, 4788], ['Код', 'Назва контролю', 'Роль', 'Як допомагає в СУМЗ'], C.nist[t.id]));
  b.push(p('D3FEND (опційно): ' + C.d3fend[t.id], { spacing: { before: 80, after: 120 }, run: { size: 18, color: '374151' } }));
}

b.push(new Paragraph({ children: [new PageBreak()] }));
b.push(h('5. Розміщення контролів в архітектурі СУМЗ', HeadingLevel.HEADING_1));
b.push(p(C.placementIntro));
b.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({
  type: 'png', data: fs.readFileSync('dfd_controls.png'), transformation: { width: 640, height: 426 },
  altText: { title: 'DFD СУМЗ з контролями', description: 'DFD СУМЗ з межами довіри TB1-TB5 і мітками контролів NIST SP 800-53 для трьох загроз', name: 'dfd-controls' },
})] }));
b.push(p('Рисунок 1. DFD СУМЗ з ДЗ2: мітки показують, де працює кожен контроль.', { alignment: AlignmentType.CENTER, run: { italics: true, size: 18 } }));
b.push(table([1250, 650, 2150, 2838, 1000, 1750], ['Контроль', 'Загр.', 'Рівень / компонент DFD', 'Реалізація', 'MVP', 'Ресурси'], C.placement));
b.push(h('Що можна зробити в MVP і що потребує ресурсів', HeadingLevel.HEADING_2));
C.mvp.forEach(t => b.push(bullet(t)));

b.push(h('6. Висновок', HeadingLevel.HEADING_1));
b.push(table([2300, W - 2300], ['Питання', 'Відповідь'], C.conclusion, { size: 18 }));

b.push(h(C.extra.title, HeadingLevel.HEADING_1));
b.push(p(C.extra.intro));
b.push(h('Як змінюються загрози', HeadingLevel.HEADING_2));
b.push(table([900, 5238, 3500], ['STRIDE', 'Нова або змінена загроза', 'ATT&CK'], C.extra.threats));
b.push(h('Які контролі додати або посилити', HeadingLevel.HEADING_2));
b.push(table([1300, 2600, 5738], ['Код', 'Назва', 'Що змінюється'], C.extra.controls));

b.push(h('Зведена матриця трасування', HeadingLevel.HEADING_1));
b.push(table([1650, 850, 1900, 1900, 1588, 1750], ['Загроза', 'STRIDE', 'ATT&CK', 'NIST SP 800-53', 'Рівень', 'MVP'], C.trace));

const doc = new Document({
  creator: 'Фарід Джафарлі', title: C.title,
  styles: { default: { document: { run: { font: FONT, size: 21 } } }, paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, color: '1F3A8A', font: FONT }, paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 23, bold: true, color: '1F2937', font: FONT }, paragraph: { spacing: { before: 220, after: 100 }, outlineLevel: 1 } },
  ] },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } }, children: b }],
});
const out = 'ДЗ5_Джафарлі_Фарід.docx';
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(out, buf); console.log('written', out, buf.length); });
