## Workflow

1. **Ветки**:
   - `main`: Production-ready код.
   - `dev`: Ветка для разработки.
   - `feature/*`: Ветки для новых функций.

2. **Процесс разработки**:
   - Создайте feature-ветку от `dev`:
     ```bash
     git checkout dev
     git pull origin dev
     git checkout -b feature/your-feature-name
     ```
   - Делайте коммиты и пушите изменения:
     ```bash
     git add .
     git commit -m "Описание изменений"
     git push -u origin feature/your-feature-name
     ```
   - Создайте Pull Request (PR) из feature-ветки в `dev`.
   - Назначьте ревьювера.
   - После одобрения PR, слейте изменения в `dev`.

3. **Релиз**:
   - Когда `dev` стабилизируется, создайте PR из `dev` в `main`.
   - После ревью и одобрения слейте изменения.

4. **Ревью**:
   - Если во время презентации что-то сломается, ревьювер теряет 10% оценки.
   - Если всё работает, ревьювер получает +10% к оценке.