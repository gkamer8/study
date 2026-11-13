// Simple markdown renderer with GFM tables, ^superscript^, images and figures.
//
// Code spans, backslash escapes, images and links are swapped out for placeholders
// before emphasis runs, so `*` and `_` inside code, URLs, alt text or IDs such as
// NM_000546.6 are never turned into <em>. Underscore emphasis only applies at word
// boundaries (as in GFM). A paragraph whose first line is only an image becomes
// <figure><img><figcaption>rest of paragraph</figcaption></figure>.

const P = '\u0000';

export const Markdown = {
    render(text) {
        if (!text) return '';
        const store = [];
        const keep = (html) => `${P}${store.push(html) - 1}${P}`;
        const attr = (s) => s.replace(/"/g, '&quot;');

        let html = text;

        // Escape HTML
        html = html.replace(/&/g, '&amp;')
                   .replace(/</g, '&lt;')
                   .replace(/>/g, '&gt;');

        // Code blocks (fenced with ```) and inline code: protect contents
        html = html.replace(/```([^`]+)```/g, (m, c) => keep(`<pre><code>${c}</code></pre>`));
        html = html.replace(/`([^`]+)`/g, (m, c) => keep(`<code>${c}</code>`));

        // Backslash escapes (\* \_ \[ etc.)
        html = html.replace(/\\([\\`*_{}\[\]()#+\-.!|^])/g, (m, c) => keep(c));

        const inline = (s) => {
            // Images, then links (text may contain emphasis; URL is protected)
            s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g,
                (m, alt, src) => keep(`<img src="${attr(src)}" alt="${attr(alt)}" loading="lazy">`));
            s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,
                (m, t, href) => keep(`<a href="${attr(href)}" target="_blank" rel="noopener">${emph(t)}</a>`));
            return emph(s);
        };
        const emph = (s) => {
            s = s.replace(/\*\*(?=\S)([^\n]+?)\*\*/g, '<strong>$1</strong>');
            s = s.replace(/(^|[^\w])__([^_\n]+)__(?!\w)/g, '$1<strong>$2</strong>');
            s = s.replace(/\*([^*\n]+)\*/g, '<em>$1</em>');
            s = s.replace(/(^|[^\w])_([^_\n]+)_(?!\w)/g, '$1<em>$2</em>');
            s = s.replace(/\^([^\^\n]+)\^/g, '<sup>$1</sup>');
            return s;
        };

        // Figures: a block whose first line is a lone image; the rest is the caption
        html = html.split('\n\n').map(block => {
            const m = block.trim().match(/^!\[([^\]]*)\]\(([^)\s]+)\)[ \t]*(?:\n([\s\S]*))?$/);
            if (!m) return block;
            const img = `<img src="${attr(m[2])}" alt="${attr(m[1])}" loading="lazy">`;
            const cap = m[3] && m[3].trim() ? `<figcaption>${inline(m[3].trim())}</figcaption>` : '';
            return keep(`<figure>${img}${cap}</figure>`);
        }).join('\n\n');

        // Headers
        html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');

        // Inline markup everywhere else
        html = inline(html);

        // Tables (GFM-style)
        html = this.renderTables(html);

        // Lists
        html = this.renderLists(html);

        // Paragraphs
        html = html.split('\n\n').map(para => {
            para = para.trim();
            if (!para) return '';
            if (para.startsWith('<')) return para; // Already HTML
            if (/^\u0000\d+\u0000$/.test(para) && store[+para.slice(1, -1)].startsWith('<figure')) return para;
            return `<p>${para}</p>`;
        }).join('\n');

        // Restore protected pieces (they may nest)
        const re = /\u0000(\d+)\u0000/g;
        while (re.test(html)) html = html.replace(re, (m, i) => store[+i]);

        return html;
    },

    renderTables(html) {
        const lines = html.split('\n');
        const result = [];
        let i = 0;

        while (i < lines.length) {
            const line = lines[i];
            
            // Check if this looks like a table header
            if (line.includes('|') && i + 1 < lines.length && lines[i + 1].match(/^\|?[\s\-:|]+\|?$/)) {
                const headers = line.split('|').map(h => h.trim()).filter(h => h);
                const separator = lines[i + 1];
                
                let tableHtml = '<table>\n<thead>\n<tr>';
                headers.forEach(h => {
                    tableHtml += `<th>${h}</th>`;
                });
                tableHtml += '</tr>\n</thead>\n<tbody>\n';

                i += 2; // Skip header and separator

                // Read table rows
                while (i < lines.length && lines[i].includes('|')) {
                    const cells = lines[i].split('|').map(c => c.trim()).filter(c => c);
                    if (cells.length > 0) {
                        tableHtml += '<tr>';
                        cells.forEach(c => {
                            tableHtml += `<td>${c}</td>`;
                        });
                        tableHtml += '</tr>\n';
                    }
                    i++;
                }

                tableHtml += '</tbody>\n</table>';
                result.push(tableHtml);
            } else {
                result.push(line);
                i++;
            }
        }

        return result.join('\n');
    },

    renderLists(html) {
        const lines = html.split('\n');
        const result = [];
        let i = 0;

        while (i < lines.length) {
            const line = lines[i];
            const unorderedMatch = line.match(/^[\*\-] (.+)$/);
            const orderedMatch = line.match(/^\d+\. (.+)$/);

            if (unorderedMatch || orderedMatch) {
                const isOrdered = !!orderedMatch;
                const tag = isOrdered ? 'ol' : 'ul';
                let listHtml = `<${tag}>\n`;

                while (i < lines.length) {
                    const currentLine = lines[i];
                    const ulMatch = currentLine.match(/^[\*\-] (.+)$/);
                    const olMatch = currentLine.match(/^\d+\. (.+)$/);
                    
                    if ((isOrdered && olMatch) || (!isOrdered && ulMatch)) {
                        const content = (ulMatch || olMatch)[1];
                        listHtml += `<li>${content}</li>\n`;
                        i++;
                    } else {
                        break;
                    }
                }

                listHtml += `</${tag}>`;
                result.push(listHtml);
            } else {
                result.push(line);
                i++;
            }
        }

        return result.join('\n');
    }
};
