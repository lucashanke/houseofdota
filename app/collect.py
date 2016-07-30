from services.collector_service import CollectorService

def main():
    very_high_collector = CollectorService(3, ap=True, rap=True)
    matches_recorded =very_high_collector.collect_from_last_100()

if __name__ == "__main__":
    main()
