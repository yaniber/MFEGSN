# Guide Google Colab - MFEGSN

Ce guide explique comment utiliser MFEGSN sur Google Colab pour importer des PDFs depuis Google Drive et sauvegarder les résultats.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yaniber/MFEGSN/blob/main/MFEGSN_Colab.ipynb)

## 🎯 Avantages de Google Colab

- **Aucune installation** : Tout fonctionne dans le cloud
- **Gratuit** : Accès gratuit avec GPU si nécessaire
- **Google Drive** : Import et export faciles
- **Partage** : Partagez facilement vos notebooks
- **Persistance** : Sauvegardez vos résultats facilement

## 📤 Importer des PDFs depuis Google Drive

### Étape 1 : Monter Google Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

Cela vous demandera d'autoriser l'accès à votre Drive.

### Étape 2 : Configurer le chemin vers vos PDFs

```python
# Modifiez ce chemin selon l'emplacement de vos PDFs dans Drive
GDRIVE_PDF_FOLDER = "/content/drive/MyDrive/PDFs"
```

**Comment trouver le bon chemin ?**

1. Ouvrez votre Google Drive dans votre navigateur
2. Naviguez vers le dossier contenant vos PDFs
3. Le chemin sera de la forme : `/content/drive/MyDrive/NomDuDossier`
4. Pour un dossier partagé : `/content/drive/Shareddrives/NomDuDossier`

### Étape 3 : Importer les PDFs

Le notebook copiera automatiquement tous les fichiers PDF du dossier spécifié vers le répertoire de travail Colab.

## 💾 Sauvegarder les Outputs

Vous avez trois options pour sauvegarder vos résultats :

### Option 1 : Sauvegarder vers Google Drive (Recommandé)

**Avantages :**
- Simple et rapide
- Persistant même après fermeture du notebook
- Accessible depuis n'importe où

**Instructions :**

```python
import shutil
from pathlib import Path
from datetime import datetime

# Chemin de destination dans Drive
GDRIVE_OUTPUT_FOLDER = "/content/drive/MyDrive/MFEGSN_Outputs"

# Créer un dossier avec timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = Path(GDRIVE_OUTPUT_FOLDER) / f"output_{timestamp}"
output_path.mkdir(parents=True, exist_ok=True)

# Copier les résultats
shutil.copytree("markdown_outputs", output_path / "markdown_outputs")
shutil.copytree("chroma_db", output_path / "chroma_db")
```

**Résultat :**
- Vos fichiers Markdown extraits
- Votre base de données vectorielle
- Organisés par date et heure

### Option 2 : Sauvegarder vers GitHub (Nouvelle Branche)

**Avantages :**
- Versioning avec Git
- Collaboration facile
- Traçabilité complète

**Instructions :**

#### 1. Créer un Personal Access Token GitHub

1. Allez sur : https://github.com/settings/tokens
2. Cliquez sur "Generate new token" → "Generate new token (classic)"
3. Donnez un nom descriptif (ex: "Colab MFEGSN")
4. Cochez les permissions :
   - `repo` (accès complet aux repositories)
5. Cliquez sur "Generate token"
6. **IMPORTANT** : Copiez le token immédiatement (vous ne pourrez plus le voir)

#### 2. Configurer Git dans Colab

```python
# Configurez avec vos informations
!git config --global user.email "votre-email@example.com"
!git config --global user.name "Votre Nom"
```

#### 3. Créer une nouvelle branche et commiter

```python
from datetime import datetime

# Créer une branche avec timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
branch_name = f"colab-outputs-{timestamp}"

# Créer et basculer vers la nouvelle branche
!git checkout -b {branch_name}

# Ajouter les fichiers
!git add markdown_outputs/ chroma_db/ pdfs/

# Commiter
!git commit -m "Add Colab outputs from {timestamp}"
```

#### 4. Pousser vers GitHub

```bash
# Remplacez YOUR_TOKEN par votre token GitHub
# Remplacez yaniber par votre nom d'utilisateur si vous avez forké le repo
!git push https://YOUR_TOKEN@github.com/yaniber/MFEGSN.git {branch_name}
```

**⚠️ Sécurité :** 
- Ne commitez JAMAIS votre token dans le code
- Utilisez-le uniquement dans Colab
- Révoquezle token après utilisation si nécessaire

#### 5. Créer une Pull Request

1. Allez sur GitHub : https://github.com/yaniber/MFEGSN
2. Vous verrez un message proposant de créer une Pull Request pour votre nouvelle branche
3. Cliquez sur "Compare & pull request"
4. Ajoutez une description : "Outputs from Google Colab - [date]"
5. Créez la Pull Request

**Résultat :**
- Une nouvelle branche avec vos outputs
- Une PR prête à être mergée
- Historique complet des modifications

### Option 3 : Télécharger Localement

**Simple et rapide pour une sauvegarde locale :**

```python
from google.colab import files
import shutil
from datetime import datetime

# Créer une archive ZIP
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
archive_name = f"mfegsn_outputs_{timestamp}"

shutil.make_archive(archive_name, 'zip', '.', 'markdown_outputs')

# Télécharger
files.download(f"{archive_name}.zip")
```

## 🔄 Workflow Complet Recommandé

### Pour un Usage Personnel

1. **Import** : Montez Drive → Importez PDFs
2. **Traitement** : Extrayez et indexez
3. **Recherche** : Testez vos requêtes
4. **Sauvegarde** : Sauvegardez vers Drive

### Pour la Collaboration

1. **Import** : Uploadez ou importez depuis Drive
2. **Traitement** : Extrayez et indexez
3. **Validation** : Vérifiez les résultats
4. **GitHub** : Poussez vers une nouvelle branche
5. **Pull Request** : Demandez une review

## 📊 Que Sauvegarder ?

### Fichiers Générés

1. **markdown_outputs/** : 
   - Contenu extrait des PDFs en Markdown
   - Un fichier par PDF
   - Conserve la structure et le formatage

2. **chroma_db/** :
   - Base de données vectorielle
   - Embeddings des documents
   - Nécessaire pour les recherches sémantiques

3. **pdfs/** :
   - Les fichiers PDF originaux
   - Optionnel (peut être volumineux)

### Recommandations

- **Toujours sauvegarder** : `markdown_outputs/` et `chroma_db/`
- **Optionnel** : `pdfs/` (sauf si vous voulez un backup complet)
- **Ignorer** : Fichiers temporaires, logs

## 🔒 Bonnes Pratiques

### Sécurité

- ✅ Utilisez des Personal Access Tokens pour GitHub
- ✅ Ne partagez jamais vos tokens
- ✅ Révoquez les tokens après usage si nécessaire
- ✅ Utilisez des permissions minimales

### Organisation

- ✅ Utilisez des timestamps dans les noms de branches/dossiers
- ✅ Documentez vos Pull Requests
- ✅ Nettoyez les anciennes branches régulièrement
- ✅ Organisez vos dossiers Drive par projet/date

### Performance

- ✅ Traitez les PDFs par lots si vous en avez beaucoup
- ✅ Utilisez GPU Colab pour un traitement plus rapide
- ✅ Sauvegardez régulièrement (Colab peut se déconnecter)

## 🆘 Dépannage

### "No space left on device"

Colab a un espace disque limité. Solutions :
1. Traitez moins de PDFs à la fois
2. Sauvegardez et nettoyez régulièrement
3. Utilisez Colab Pro pour plus d'espace

### "Session disconnected"

Colab se déconnecte après inactivité. Solutions :
1. Sauvegardez régulièrement vers Drive
2. Utilisez Colab Pro pour des sessions plus longues
3. Gardez l'onglet Colab actif

### "Permission denied" sur GitHub

Vérifiez :
1. Votre token est valide
2. Vous avez les permissions `repo`
3. Le token n'a pas expiré

### "No module named..."

Réexécutez la cellule d'installation :
```python
!pip install -q -r requirements.txt
```

## 📚 Ressources

- [Documentation Colab](https://colab.research.google.com/)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [README Principal](README.md)

## 💡 Conseils

- **Nommez vos branches** de manière descriptive (ex: `colab-research-papers-20240115`)
- **Testez d'abord** avec quelques PDFs avant de traiter un gros lot
- **Documentez** vos Pull Requests avec le contexte
- **Communiquez** avec l'équipe avant de merger de gros changements

Besoin d'aide ? Ouvrez une issue sur GitHub !
