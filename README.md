# JustPay API

JustPay est une API bancaire développée avec FastAPI et SQLModel. Elle permet la gestion des utilisateurs, comptes bancaires, bénéficiaires et paiements (virements internes et externes).

## Fonctionnalités

- **Authentification** : Création et connexion d’utilisateurs.
- **Gestion des utilisateurs** : CRUD sur les profils.
- **Comptes bancaires** : Création, consultation, mise à jour, suppression, dépôt et consultation du solde.
- **Bénéficiaires** : Ajout, consultation, modification, suppression et listing des bénéficiaires.
- **Paiements** : Virements internes (entre comptes d’un même utilisateur) et externes (vers d’autres comptes), consultation et annulation de paiements.

## Endpoints principaux

| Ressource      | Méthode | Route                                 | Description                                 |
|----------------|---------|---------------------------------------|---------------------------------------------|
| Auth           | POST    | `/auth/register`                      | Inscription utilisateur                     |
| Auth           | POST    | `/auth/login`                         | Connexion utilisateur                       |
| Utilisateur    | GET     | `/users/{user_id}`                    | Voir un utilisateur                         |
| Utilisateur    | PUT     | `/users/{user_id}`                    | Modifier un utilisateur                     |
| Utilisateur    | DELETE  | `/users/{user_id}`                    | Supprimer un utilisateur                    |
| Comptes        | POST    | `/bankaccount/accounts/primary`       | Créer un compte principal                   |
| Comptes        | POST    | `/bankaccount/accounts/secondary`     | Créer un compte secondaire                  |
| Comptes        | GET     | `/bankaccount/accounts/primary/{user_id}` | Voir le compte principal                |
| Comptes        | GET     | `/bankaccount/accounts/secondary/{user_id}` | Voir les comptes secondaires            |
| Comptes        | GET     | `/bankaccount/accounts/`              | Voir tous les comptes                       |
| Comptes        | PUT     | `/bankaccount/accounts/{account_number}` | Modifier un compte                      |
| Comptes        | DELETE  | `/bankaccount/accounts/{account_number}` | Supprimer un compte                     |
| Bénéficiaires  | POST    | `/beneficiaries/`                     | Ajouter un bénéficiaire                     |
| Bénéficiaires  | GET     | `/beneficiaries/{beneficiary_id}`     | Voir un bénéficiaire                        |
| Bénéficiaires  | PUT     | `/beneficiaries/{beneficiary_id}`     | Modifier un bénéficiaire                    |
| Bénéficiaires  | DELETE  | `/beneficiaries/{beneficiary_id}`     | Supprimer un bénéficiaire                   |
| Bénéficiaires  | GET     | `/beneficiaries/user/{user_id}`       | Voir tous les bénéficiaires d’un utilisateur|
| Paiements      | POST    | `/payments/internal`                  | Virement interne                            |
| Paiements      | POST    | `/payments/external`                  | Virement externe                            |
| Paiements      | GET     | `/payments/{payment_id}`              | Voir un paiement                            |
| Paiements      | GET     | `/payments/account/{account_number}`  | Voir les paiements d’un compte              |
| Paiements      | POST    | `/payments/cancel`                    | Annuler un paiement                         |

## Démarrage

1. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Lance l’API :
   ```bash
   uvicorn main:app --reload
   ```
3. Accède à la documentation interactive :
   ```
   http://localhost:8000/docs
   ```

## Technologies

- Python 3.13+
- FastAPI
- SQLModel
- SQLite (par défaut)

## Structure du projet

```
.
├── main.py
├── db/
│   ├── models.py
│   ├── database.py
├── routes/
│   ├── user/
│   ├── bankAccount/
│   ├── beneficiary/
│   ├── payement/
│   ├── auth/
├── payment.py
├── bankAccount.py
├── beneficiary.py
├── user.py
└── README.md
```

## Auteur

JustPay Team

---

Pour toute question, consulte la documentation FastAPI ou contacte l’équipe JustPay.