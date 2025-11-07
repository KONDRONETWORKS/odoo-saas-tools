
# Expression de Besoin – Application de Gestion de Trésorerie et Workflow de Paiement

## 1. Contexte et Objectif

L’entreprise souhaite disposer d’une application interne permettant :
- D’enregistrer et de suivre tous les mouvements de trésorerie (caisse, banque, Djamo)
- De retracer les mouvements bancaires à partir des saisies réalisées par l’assistante
- De mettre en place un workflow complet de validation et d’exécution des paiements fournisseurs, aussi bien pour les dépenses internes que pour les dépenses liées à des projets commerciaux

**Objectif** :  
Assurer une traçabilité complète des flux financiers, une meilleure visibilité sur la trésorerie et un contrôle rigoureux des dépenses à travers un processus automatisé et structuré.

---

## 2. Fonctionnalités principales

### 2.1. Gestion de la trésorerie

- Enregistrement des mouvements de caisse, banque et Djamo.
- Chaque compte affiche un tableau à deux colonnes :
    - **Entrées** : recettes, dépôts, paiements reçus
    - **Sorties** : décaissements, paiements fournisseurs, retraits, notes de frais
- Filtre par période, type de compte, ou nature de dépense.
- Calcul automatique du solde courant :  
  `solde courant = solde initial + entrées – sorties`

### 2.2. Suivi des mouvements bancaires

- Saisie des opérations bancaires par l’assistante :
    - **Date**
    - **Sens** (entrée/sortie)
    - **Montant**
    - **Méthode** (virement, chèque, cash, mobile money)
    - **Bénéficiaire**
    - **Référence**
    - **Commentaire**
    - **Pièces justificatives** (scannées : relevé, virement, chèque, etc.)
- Chaque saisie alimente automatiquement le compte “Banque de l’entreprise”.

---

## 3. Workflow de paiement fournisseur

### Deux types de paiements à gérer :

#### **A. Paiement dans le cadre d’une dépense interne**

1. **Création de la demande de dépense interne**
    - Objet de la demande
    - Service demandeur
    - Montant estimé / budget concerné
    - Description de la dépense
    - Pièces jointes (devis, justificatif, etc.)
2. **Validation hiérarchique**
    - Soumission à une instance supérieure pour validation
3. **Planification bancaire**
    - Montant inscrit dans une ligne de décaissement planifiée au niveau de la banque
4. **Exécution du paiement**
    - Méthode de paiement (cash, virement, chèque)
    - Date de paiement
    - Nom du fournisseur
    - Référence du paiement
    - Compte bancaire de l’entreprise utilisé
    - Génère automatiquement une écriture dans le compte banque (“sortie”)
5. **Clôture de la demande**
    - Dépense passe à l’état “Payée” puis “Clôturée”

#### **B. Paiement dans le cadre d’une activité commerciale**

Chaque projet est rattaché à un dossier commercial numérique incluant :

- **Informations générales**
    - Numéro du dossier  
    - Nom du client  
    - Commercial responsable  
    - Chef de projet  
    - Ingénieur principal  
    - Description du projet  
    - Durée de réalisation  
    - Nature du projet : vente de matériel / vente de services / mixte  
- **Documents associés**
    - Devis
    - Bon de commande du client (scanné)
    - Facture client
    - Notes de frais
    - Bons de commande fournisseurs
    - Factures fournisseurs
- **Dépenses liées au projet**
    - Type (fournisseur ou note de frais)
    - Montant
    - Fournisseur ou employé concerné
    - Description / référence
    - Pièce jointe (facture, bon, reçu)
    - *Workflow de validation* :
        > Soumise → Validée par le chef de projet → Approuvée par la direction → Planifiée → Payée
- **Enregistrement dans les comptes**
    - Les paiements sont automatiquement intégrés dans le compte concerné (banque, caisse ou Djamo)
    - Chaque écriture indique : date, sens, montant, méthode, fournisseur, projet lié

---

## 4. Rapports et Tableaux de Bord

L’application doit permettre de générer :
- Un état de la trésorerie (solde caisse, banque, Djamo)
- Le plan de décaissement à venir (par date, fournisseur, statut)
- Le suivi des dépenses internes (par service, période ou nature)
- Le suivi des projets commerciaux (budget vs dépenses engagées vs payées)
- Le journal complet des écritures avec filtres et exports Excel/PDF

---

## 5. Workflow global des processus

### **A. Dépense interne**
```
Brouillon → Soumise → Validée → Planifiée → Payée → Clôturée
```
### **B. Dépense commerciale**
```
Création dossier → Ajout dépenses → Validation → Planification → Paiement → Suivi projet
```

---

## 6. Rôles et Permissions

- **Assistante** : saisie des mouvements (banque, caisse, Djamo), pièces jointes
- **Chef de service** : création et validation des dépenses internes
- **Chef de projet** : validation des dépenses liées à un projet
- **DAF / Direction** : approbation finale et validation de paiement
- **Comptable** : rapprochements, corrections et éditions de rapports
- **Lecture seule (audit)** : consultation des historiques

---

## 7. Exigences Techniques

- Application web (responsive) et/ou mobile interne
- Base de données centralisée avec traçabilité des actions
- Historique des validations (qui a validé, quand, avec quel commentaire)
- Gestion des pièces jointes (PDF, JPG, PNG) avec horodatage
- Exports Excel/PDF
- Possibilité d’évoluer vers :
    - Intégration avec Odoo (comptabilité)
    - Import automatique de relevés bancaires ou Djamo
    - Système de notifications internes (mails, alertes)

---

## 8. Livrables Attendus

- Version MVP incluant :
    - Comptes (Banque, Caisse, Djamo)
    - Workflow complet de dépense interne et projet
    - Dossiers commerciaux numériques
    - Rapports de trésorerie et plan de décaissement
- Documentation technique et utilisateur
- Accès administrateur pour création/modification de comptes, rôles, utilisateurs

---

## Souhaits de mise en œuvre

- Interface intuitive et simple d’utilisation, adaptée à une assistante et un comptable
- Traçabilité complète des flux financiers et suivi en temps réel des dépenses et soldes
- Architecture évolutive pour intégration future avec d’autres outils internes (Odoo, CRM, etc.)
