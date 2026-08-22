name: Run Ginesys Bot Workflow

on:
  repository_dispatch:
    types: [run-ginesys-step]
  workflow_dispatch:
  schedule:
    - cron: '0 * * * *'

jobs:
  run-bot:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install playwright pandas openpyxl
          playwright install chromium
          playwright install-deps

      - name: Run Ginesys Bot Script
        run: |
          python bot.py ${{ github.event.client_payload.step || 'step2' }}

      - name: Commit and Push Generated Files
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add billing_data.xlsx downloads/ data.json || true
          git commit -m "Auto generated Ginesys files & reports" || exit 0
          git push
