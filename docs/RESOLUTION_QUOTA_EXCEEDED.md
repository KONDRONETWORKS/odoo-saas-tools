# Résolution de l'Erreur "The quota has been exceeded"

## 🔍 Problème

Erreur `QuotaExceededError: The quota has been exceeded` lors de l'installation d'un module.

**Cause :** Le localStorage du navigateur est plein (limite généralement de 5-10 Mo).

## ✅ Solutions

### Solution 1 : Vider le localStorage (Recommandée)

**Dans la console du navigateur (F12) :**

```javascript
// Vider complètement le localStorage
localStorage.clear();
sessionStorage.clear();

// Recharger la page
location.reload();
```

**OU manuellement :**

1. Ouvrir les DevTools (F12)
2. Onglet **Application** (Chrome) ou **Storage** (Firefox)
3. **Local Storage** > `http://localhost:8069`
4. Clic droit > **Clear** ou **Supprimer**
5. Faire de même pour **Session Storage**
6. Recharger la page (F5)

### Solution 2 : Navigation privée

Tester dans une fenêtre de navigation privée pour éviter le localStorage :

- **Chrome/Edge** : `Ctrl+Shift+N` (Windows) ou `Cmd+Shift+N` (Mac)
- **Firefox** : `Ctrl+Shift+P` (Windows) ou `Cmd+Shift+P` (Mac)
- **Safari** : `Cmd+Shift+N`

### Solution 3 : Désactiver temporairement le mode dev

Le mode `--dev=all` génère beaucoup de données de debug qui remplissent le localStorage.

**Option A : Retirer `--dev=all` temporairement**

```yaml
# Dans config/docker-compose.simple.yml
command: >
  odoo
  --config=/etc/odoo/odoo.conf
  # ... autres options
  # --dev=all  # Commenter cette ligne
```

Puis redémarrer :
```bash
docker compose -f config/docker-compose.simple.yml restart odoo
```

**Option B : Garder le mode dev mais vider régulièrement le localStorage**

### Solution 4 : Augmenter la limite (Non recommandé)

⚠️ **Cette solution n'est pas recommandée** car elle nécessite de modifier les paramètres du navigateur et peut causer des problèmes de performance.

## 🔧 Script de Nettoyage Automatique

Ajoutez ce script dans la console du navigateur pour nettoyer automatiquement :

```javascript
// Nettoyer le localStorage si trop plein
function cleanLocalStorage() {
    const keys = Object.keys(localStorage);
    const size = JSON.stringify(localStorage).length;
    
    if (size > 4 * 1024 * 1024) { // 4 Mo
        console.log('Nettoyage du localStorage...');
        // Garder seulement les clés essentielles
        const essentialKeys = ['odoo.session_id', 'odoo.user_id'];
        keys.forEach(key => {
            if (!essentialKeys.includes(key)) {
                localStorage.removeItem(key);
            }
        });
        console.log('✅ Nettoyage terminé');
    }
}

// Exécuter au chargement
cleanLocalStorage();
```

## 📋 Checklist de Résolution

- [ ] Vider le localStorage via DevTools (Solution 1)
- [ ] Vider le sessionStorage également
- [ ] Recharger la page (F5)
- [ ] Si problème persiste : Tester en navigation privée (Solution 2)
- [ ] Si toujours problème : Désactiver temporairement `--dev=all` (Solution 3)

## 💡 Prévention

Pour éviter ce problème à l'avenir :

1. **Vider régulièrement le localStorage** lors du développement
2. **Utiliser la navigation privée** pour les tests
3. **Limiter l'utilisation de `--dev=all`** si ce n'est pas nécessaire
4. **Surveiller la taille du localStorage** avec DevTools

## 🚀 Après le Nettoyage

Une fois le localStorage vidé :

1. Recharger la page Odoo
2. Réessayer l'installation du module `saas_portal`
3. L'installation devrait fonctionner normalement

