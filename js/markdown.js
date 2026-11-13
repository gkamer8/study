// Simple markdown renderer with GFM tables and ^superscript^ support

export const Markdown = {
    render(text) {
        if (!text) return '';

        let html = text;

        // Escape HTML
        html = html.replace(/&/g, '&amp;')
                   .replace(/</g, '&lt;')
                   .replace(/>/g, '&gt;');

        // Headers
        html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');

        // Bold
        html = html.replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/__([^_]+)__/g, '<strong>$1</strong>');

        // Italic
        html = html.replace(/\*([^\*]+)\*/g, '<em>$1</em>');
        html = html.replace(/_([^_]+)_/g, '<em>$1</em>');

        // Superscript (^text^)
        html = html.replace(/\^([^\^]+)\^/g, '<sup>$1</sup>');

        // Code blocks (fenced with ```)
        html = html.replace(/```([^`]+)```/g, '<pre><code>$1</code></pre>');

        // Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Links
        html = html.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Tables (GFM-style)
        html = this.renderTables(html);

        // Lists
        html = this.renderLists(html);

        // Paragraphs
        html = html.split('\n\n').map(para => {
            para = para.trim();
            if (!para) return '';
            if (para.startsWith('<')) return para; // Already HTML
            return `<p>${para}</p>`;
        }).join('\n');

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
