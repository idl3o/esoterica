# Deploying Synthesis Library to Vercel

## 🚀 Quick Deploy

### Option 1: Deploy from Git (Recommended)

1. **Commit your changes:**
```bash
git add .
git commit -m "Add synthesis library with mobile infinite scroll"
git push
```

2. **Deploy to Vercel:**
```bash
vercel --prod
```

That's it! Vercel will:
- ✅ Automatically run `npm run build` (builds synthesis-index.json)
- ✅ Deploy all synthesis markdown files
- ✅ Deploy the library HTML and index
- ✅ Set up routes for clean URLs

### Option 2: Deploy via Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your Git repository
3. Vercel auto-detects settings from `vercel.json`
4. Click "Deploy"

---

## 📍 Access URLs

After deployment, your library will be available at:

```
https://your-project.vercel.app/library
https://your-project.vercel.app/synthesis-library
```

Your existing routes remain:
```
https://your-project.vercel.app/constellation/...
https://your-project.vercel.app/distillations/...
```

---

## 🔧 Configuration

### What's Configured

The `vercel.json` now includes:

1. **Build Command**: `npm run build`
   - Runs `build-synthesis-index.js` automatically
   - Generates fresh `synthesis-index.json` on each deploy

2. **Static Assets**:
   - `synthesis-library.html` (the library interface)
   - `synthesis-index.json` (generated index)
   - `synthesis/**/*.md` (all source documents)

3. **Routes**:
   - `/library` → synthesis-library.html
   - `/synthesis-library` → synthesis-library.html
   - `/synthesis/*` → individual markdown files

### What Gets Deployed

```
✅ synthesis-library.html         (42KB)
✅ synthesis-index.json            (generated during build)
✅ synthesis/**/*.md               (180 documents, ~500KB)
✅ build-synthesis-index.js        (index builder)
✅ constellation/**                (existing)
✅ distillations/**                (existing)
✅ api/**                          (existing)
```

---

## 🔄 Automatic Rebuilding

Every time you deploy, Vercel will:
1. Run `npm run build`
2. Scan all files in `synthesis/`
3. Generate fresh `synthesis-index.json`
4. Deploy updated library

This means:
- ✅ Add new documents → just deploy
- ✅ Edit existing documents → just deploy
- ✅ Index is always up-to-date
- ✅ No manual rebuild needed

---

## 📝 Adding New Documents

1. **Add markdown file** to `synthesis/category/`:
```bash
# Example
synthesis/breakthroughs/my-new-recognition.md
```

2. **Commit and deploy**:
```bash
git add synthesis/breakthroughs/my-new-recognition.md
git commit -m "Add new recognition document"
git push
vercel --prod
```

3. **Index rebuilds automatically** during deployment

4. **Library updates** with new document immediately

---

## 🧪 Testing Before Deploy

### Local Test
```bash
# Rebuild index locally
npm run build

# Start local server
python3 -m http.server 8000

# Test at http://localhost:8000/synthesis-library.html
```

### Vercel Preview
```bash
# Deploy to preview URL (not production)
vercel

# Get a unique preview URL to test
# Example: https://esoterica-xyz123.vercel.app
```

---

## 🎯 Deployment Checklist

Before deploying:

- [ ] Run `npm run build` locally to verify it works
- [ ] Check that `synthesis-index.json` was created
- [ ] Test `synthesis-library.html` in local server
- [ ] Verify all synthesis documents are committed
- [ ] Review `.gitignore` to ensure nothing is excluded
- [ ] Push to Git repository
- [ ] Deploy to Vercel
- [ ] Test live URL: `https://your-project.vercel.app/library`

---

## 🐛 Troubleshooting

### "Cannot GET /synthesis-index.json"

**Cause**: Build script didn't run or index not deployed

**Fix**:
```bash
# Check build logs in Vercel dashboard
# Ensure package.json has:
"scripts": {
  "vercel-build": "node build-synthesis-index.js"
}
```

### Documents not loading in reading view

**Cause**: Markdown files not accessible via HTTP

**Fix**: Ensure `vercel.json` includes:
```json
{
  "src": "/synthesis/(.*)",
  "dest": "/synthesis/$1"
}
```

### Index has 0 documents

**Cause**: Build script can't find synthesis folder

**Fix**:
- Check that `synthesis/` is in project root
- Verify markdown files are committed
- Check Vercel build logs for errors

### Build fails during deployment

**Cause**: Node version or missing dependencies

**Fix**: Ensure `package.json` has:
```json
"engines": {
  "node": ">=16.x"
}
```

---

## 📊 Performance on Vercel

### Expected Performance

- **Initial Load**: < 500ms (with CDN caching)
- **Search**: < 50ms (client-side filtering)
- **Document Fetch**: < 200ms (markdown files)
- **Build Time**: ~5-10 seconds (index generation)

### Optimizations Applied

- ✅ Static file deployment (no server needed)
- ✅ Vercel CDN caching
- ✅ Gzip compression automatic
- ✅ Virtual scrolling (client-side)
- ✅ Lazy loading of documents

---

## 🌍 Custom Domain (Optional)

### Add Custom Domain

1. Go to Vercel Dashboard → Settings → Domains
2. Add your domain (e.g., `library.yourdomain.com`)
3. Update DNS records as instructed
4. SSL certificate auto-generated

### Recommended Subdomains

```
library.yourdomain.com     → Synthesis Library
constellation.yourdomain.com → Constellation Explorer
docs.yourdomain.com        → Distillations
```

---

## 🔐 Environment Variables (If Needed)

If you add API features later:

```bash
# In Vercel Dashboard → Settings → Environment Variables
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

Not needed for current static deployment.

---

## 📈 Analytics (Optional)

### Add Vercel Analytics

1. Enable in Vercel Dashboard
2. Get real-time traffic data
3. See which documents are most viewed
4. Monitor search queries (client-side)

### Google Analytics

Add to `synthesis-library.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🚦 Deployment Status

### Check Build Status

```bash
# In Vercel Dashboard:
# - Green checkmark = successful deploy
# - Red X = build failed (check logs)
# - Yellow spinner = deploying
```

### View Logs

```bash
# CLI
vercel logs

# Or in Dashboard → Deployments → [deployment] → Build Logs
```

---

## 🔄 Rollback (If Needed)

### Instant Rollback

1. Go to Vercel Dashboard → Deployments
2. Find previous successful deployment
3. Click "..." → Promote to Production
4. Instant rollback (no rebuild needed)

---

## 🎉 Post-Deployment

After successful deployment:

1. **Test the library**: Visit `/library` URL
2. **Share the link**: Send to collaborators
3. **Update documentation**: Add live URL to README
4. **Monitor usage**: Check Vercel analytics

### Share These URLs

```
📚 Library:        https://your-project.vercel.app/library
✧ Constellation:   https://your-project.vercel.app/constellation/
📄 Distillations:  https://your-project.vercel.app/distillations/
```

---

## 🌟 What Users Can Do

Once deployed, users can:

- ✅ Browse all 180 documents on mobile/desktop
- ✅ Search across all content instantly
- ✅ Filter by category, tags, recognition types
- ✅ Read full documents with clean typography
- ✅ Save documents for later
- ✅ Swipe through documents (mobile)
- ✅ Explore constellation tags
- ✅ Share specific document URLs
- ✅ Access offline (with PWA setup)

---

## 🎯 Next Steps After Deploy

1. **Test on mobile** - The primary use case
2. **Share with community** - Get feedback
3. **Monitor analytics** - See what resonates
4. **Iterate based on usage** - Add requested features
5. **Add to CLAUDE.md** - Update with live URL

---

## ✨ Summary

**Deploy Command:**
```bash
vercel --prod
```

**Live URL:**
```
https://your-project.vercel.app/library
```

**Auto-Updates:**
- New documents → just push to Git
- Edited documents → just push to Git
- Index rebuilds automatically
- Zero manual maintenance

**Perfect for:**
- Mobile consciousness technology browsing
- Quick reference lookup
- Community sharing
- Personal knowledge management
- Distribution readiness

---

*"Consciousness technologies accessible anywhere, anytime, on any device."*

🌐 Ready for global access ✧
