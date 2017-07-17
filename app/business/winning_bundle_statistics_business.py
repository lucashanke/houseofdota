from app.models import WinningBundleStatistics


def calculate_from_association_rule(bundle_association_rule):

    patch_statistics = bundle_association_rule.patch_statistics
    pick_association = patch_statistics.pick_rules.filter(
        hero_bundle=bundle_association_rule.hero_bundle
    )

    if len(pick_association) is not 0:
        return WinningBundleStatistics(
            patch_statistics=patch_statistics,
            hero_bundle=bundle_association_rule.hero_bundle,
            bundle_size=bundle_association_rule.bundle_size,
            pick_rate=pick_association[0].support,
            win_rate=bundle_association_rule.confidence /
            pick_association[0].support,
            frequency=bundle_association_rule.confidence)
    return None
