# Dabbsson DBS2300 Home Assistant Integration

Dies ist eine benutzerdefinierte Integration für Home Assistant, die es Ihnen ermöglicht, Ihren Dabbsson DBS2300 Solar Generator zu überwachen und zu steuern.

## Funktionen
- Überwachung des Status Ihres DBS2300, einschließlich AC-Ausgangsleistung, DC-Ausgangsleistung, Batteriekapazität und mehr.
- Steuerung der AC-Ausgangsleistung.
- Einrichtung automatisierter Benachrichtigungen und Aktionen basierend auf dem Status des Generators.

## Installation

### Schritt 1: Installation über HACS

1. Stellen Sie sicher, dass Sie [HACS](https://hacs.xyz/) in Ihrer Home Assistant-Umgebung installiert haben.
2. Öffnen Sie HACS über die Home Assistant-Seitenleiste.
3. Klicken Sie auf "Integrations".
4. Klicken Sie auf das Dreipunkt-Menü in der oberen rechten Ecke und wählen Sie "Custom repositories".
5. Fügen Sie die URL dieses Repositorys hinzu: `https://github.com/kleimj1/homeassistant-dbs2300` und wählen Sie die Kategorie "Integration".
6. Finden Sie die neue "DBS2300"-Integration in der HACS-Integrationsliste und installieren Sie sie.

### Schritt 2: Manuelle Installation

1. Klonen oder laden Sie dieses Repository herunter.
2. Kopieren Sie das Verzeichnis `custom_components/dbs2300` in das Verzeichnis `custom_components` Ihrer Home Assistant-Installation.

### Schritt 3: Konfiguration

1. Öffnen Sie Ihr Home Assistant-Konfigurationsverzeichnis (dort, wo sich Ihre `configuration.yaml` Datei befindet).
2. Fügen Sie die folgenden Zeilen zu Ihrer `configuration.yaml` Datei hinzu:

    ```yaml
    dbs2300:
      host: !secret dbs2300_host
      device_id: !secret dbs2300_device_id
      local_key: !secret dbs2300_local_key
    ```

3. Öffnen Sie Ihre `secrets.yaml` Datei und fügen Sie die folgenden Zeilen hinzu:

    ```yaml
    dbs2300_host: 192.168.x.x  # Ersetzen Sie dies durch die tatsächliche IP-Adresse Ihres DBS2300
    dbs2300_device_id: your_device_id  # Ersetzen Sie dies durch Ihre tatsächliche Geräte-ID
    dbs2300_local_key: your_local_key  # Ersetzen Sie dies durch Ihren tatsächlichen lokalen Schlüssel
    ```

### Schritt 4: Home Assistant neu starten

1. Starten Sie Ihre Home Assistant-Instanz neu, um die neue Konfiguration zu übernehmen.

### Schritt 5: Integration überprüfen

1. Navigieren Sie nach dem Neustart zur Seite "Konfiguration" -> "Integrationen" in Home Assistant.
2. Sie sollten sehen, dass die DBS2300-Integration erfolgreich geladen wurde.
3. Fügen Sie die neuen Sensoren und Schalter nach Bedarf zu Ihrem Lovelace-Dashboard hinzu.

## Beispielautomation

Hier ist ein Beispiel, wie Sie eine Automation einrichten können, um eine Benachrichtigung zu senden, wenn die AC-Ausgangsleistung eingeschaltet wird:

```yaml
automation:
  - alias: Benachrichtigung, wenn AC-Ausgangsleistung eingeschaltet wird
    trigger:
      platform: state
      entity_id: switch.dbs2300_ac_output
      to: 'on'
    action:
      service: notify.notify
      data:
        message: "Die AC-Ausgangsleistung des DBS2300 wurde eingeschaltet."
