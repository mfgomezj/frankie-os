/**
 * Mock of n8n "Parse Frontmatter + Render HTML" node logic
 */

function mockMdToHtml(md) {
    const rows = md.split('\n').map(l => l.replace('\r', ''));
    const out = [];
    let inList = false;

    function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    function isOrderedLine(line) {
        let i = 0;
        while (i < line.length && line[i] >= '0' && line[i] <= '9') i++;
        return i > 0 && line.slice(i, i + 2) === '. ';
    }

    for (const line of rows) {
        if (line.startsWith('### ')) { if (inList) { out.push('</ul>'); inList = false; } out.push('<h3>' + esc(line.slice(4)) + '</h3>'); continue; }
        if (line.startsWith('## ')) { if (inList) { out.push('</ul>'); inList = false; } out.push('<h2>' + esc(line.slice(3)) + '</h2>'); continue; }
        if (line.startsWith('# ')) { if (inList) { out.push('</ul>'); inList = false; } out.push('<h1>' + esc(line.slice(2)) + '</h1>'); continue; }
        if (line.startsWith('- ')) { if (!inList) { out.push('<ul>'); inList = true; } out.push('<li>' + esc(line.slice(2)) + '</li>'); continue; }
        if (isOrderedLine(line)) { if (!inList) { out.push('<ul>'); inList = true; } let i = 0; while (i < line.length && line[i] >= '0' && line[i] <= '9') i++; out.push('<li>' + esc(line.slice(i + 2)) + '</li>'); continue; }
        if (line.trim() === '---') { if (inList) { out.push('</ul>'); inList = false; } out.push('<hr/>'); continue; }
        if (line.trim() === '') { if (inList) { out.push('</ul>'); inList = false; } continue; }
        if (inList) { out.push('</ul>'); inList = false; }
        out.push('<p>' + esc(line) + '</p>');
    }
    if (inList) { out.push('</ul>'); }
    return out.join('\n');
}

function testParse(mdRaw, metaFromQueue) {
    const lines = mdRaw.split('\n').map(l => l.replace('\r', ''));
    let meta = {};
    let start = 0;

    if (lines[0] === '---') {
        let i = 1;
        for (; i < lines.length; i++) {
            if (lines[i] === '---') break;
            const line = lines[i];
            const idx = line.indexOf(':');
            if (idx > -1) {
                const key = line.slice(0, idx).trim();
                const value = line.slice(idx + 1).trim();
                meta[key] = value.replace(/^"|"$/g, '');
            }
        }
        start = i + 1;
    }
    const body = lines.slice(start).join('\n');

    const title = meta.title || metaFromQueue.slug.replace(/-/g, ' ');
    const seoTitle = meta.seo_title || `${title} | JobNearMe`;
    const metaDescription = meta.meta_description || '';
    const focusKeyword = meta.focus_keyword || metaFromQueue.slug.replace(/-/g, ' ');
    const canonicalUrl = meta.canonical_url || `${metaFromQueue.wp_base_url}/${metaFromQueue.slug}/`;
    const excerpt = meta.excerpt || metaDescription || body.split('\n').find(l => l.trim()) || title;
    const status = meta.status || metaFromQueue.status;
    const category_ids = (meta.category_ids || '').split(',').map(x => Number(x.trim())).filter(n => Number.isInteger(n));
    const tag_ids = (meta.tag_ids || '').split(',').map(x => Number(x.trim())).filter(n => Number.isInteger(n));
    const image_path = meta.image_path || '';

    return {
        ...metaFromQueue,
        title,
        seo_title: seoTitle,
        meta_description: metaDescription,
        focus_keyword: focusKeyword,
        canonical_url: canonicalUrl,
        excerpt,
        status,
        category_ids,
        tag_ids,
        image_path,
        content_html: mockMdToHtml(body)
    };
}

// --- Test Cases ---

const sampleMd = `---
title: "Digital Trafficker Remote Jobs"
image_path: "images/trafficker-remote.png"
---
# Hello World
This is a test.`;

const metaQueue = {
    slug: 'trafficker-remote',
    wp_base_url: 'https://jobnearme.online',
    status: 'draft'
};

const result = testParse(sampleMd, metaQueue);

console.log("--- TEST RESULT ---");
console.log("Image Path extracted:", result.image_path);
if (result.image_path === "images/trafficker-remote.png") {
    console.log("SUCCESS: Image path extracted correctly.");
} else {
    console.log("FAILURE: Image path NOT extracted.");
    process.exit(1);
}

const queryResult = result.image_path || result.slug;
console.log("Search Query result:", queryResult);
if (queryResult === "images/trafficker-remote.png") {
    console.log("SUCCESS: Query prioritizes image_path.");
} else {
    console.log("FAILURE: Query fallback failed.");
    process.exit(1);
}
