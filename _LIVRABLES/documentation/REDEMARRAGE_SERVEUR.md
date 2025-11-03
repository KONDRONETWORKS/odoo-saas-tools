# 🔄 Instructions de Redémarrage du Serveur Odoo

## ⚠️ IMPORTANT

Après les modifications du code Python, **vous DEVEZ redémarrer le serveur Odoo** pour que les changements soient pris en compte.

---

## 🔧 Redémarrage du Serveur

### **Option 1 : Redémarrage Complet (RECOMMANDÉ)**

```bash
# 1. Arrêter le serveur Odoo (Ctrl+C ou kill)
# Si le serveur tourne en arrière-plan, trouver et tuer le processus :
ps aux | grep odoo-bin | grep -v grep
kill -9 <PID>

# 2. Redémarrer
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
source .venv/bin/activate
python3.11 ../odoo/odoo-bin -c odoo.conf --logfile=odoo.log &
```

### **Option 2 : Recharger les Modules**

Si vous ne voulez pas redémarrer complètement, vous pouvez mettre à jour les modules :

```bash
python3.11 ../odoo/odoo-bin -c odoo.conf --stop-after-init -u saas_oauth_provider
```

Puis redémarrer normalement.

### **Option 3 : Nettoyer le Cache Python**

Parfois, Python garde les anciennes versions en cache (.pyc) :

```bash
# Supprimer les fichiers .pyc
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true

# Redémarrer le serveur
```

---

## 📋 Vérifications Après Redémarrage

### **1. Vérifier que le serveur démarre sans erreur**

```bash
tail -f odoo.log | grep -i "error\|exception\|loaded"
```

### **2. Vérifier que les modules sont chargés**

Dans les logs, cherchez :
```
Module saas_oauth_provider loaded
```

### **3. Tester l'endpoint OAuth**

```bash
curl -v http://localhost:8069/oauth2/auth
```

Ne devrait **PAS** donner d'erreur 500.

---

## 🐛 Si l'Erreur Persiste Après Redémarrage

1. **Vérifier les logs complets :**
   ```bash
   tail -100 odoo.log | grep -A 20 -i "error\|traceback"
   ```

2. **Vérifier que le fichier est bien modifié :**
   ```bash
   grep -n "urllib_urlencode" saas_oauth_provider/controllers/main.py
   ```
   Devrait montrer les lignes avec `urllib_urlencode`.

3. **Vérifier la syntaxe Python :**
   ```bash
   python3 -m py_compile saas_oauth_provider/controllers/main.py
   ```

4. **Forcer le rechargement en supprimant le cache :**
   ```bash
   rm -rf saas_oauth_provider/controllers/__pycache__
   ```

---

## ✅ Après Redémarrage

Une fois le serveur redémarré, testez à nouveau :

```
http://localhost:8069/oauth2/auth?response_type=token&client_id=<uuid>&...
```

L'erreur 500 devrait être résolue ! 🎉

