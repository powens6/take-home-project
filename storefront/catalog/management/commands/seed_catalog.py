from django.core.management.base import BaseCommand

from catalog.models import Category, Tag, Product


class Command(BaseCommand):
    """Seed the database with sample categories, tags and products."""

    help = "Populate the database with demo data"

    def handle(self, *args, **options):
        category_names = [
            "Fly Rods",
            "Fly Reels",
            "Fly Lines",
            "Flies",
            "Accessories",
        ]

        tag_names = [
            "Beginner",
            "Intermediate",
            "Expert",
            "Freshwater",
            "Saltwater",
            "Lightweight",
            "Fast Action",
            "Dry Fly",
            "Nymph",
            "Streamer",
        ]

        categories = {
            name: Category.objects.get_or_create(name=name)[0]
            for name in category_names
        }
        tags = {
            name: Tag.objects.get_or_create(name=name)[0]
            for name in tag_names
        }

        products_payload = [
            ("RiverMaster 9' 5 wt Graphite Rod", "Smooth-loading rod ideal for trout on medium rivers.", "Fly Rods", ["Beginner", "Freshwater", "Lightweight"]),
            ("SaltPro 9' 8 wt Fast-Action Rod", "Salt-rated blank with extra backbone for windy flats.", "Fly Rods", ["Expert", "Saltwater", "Fast Action"]),
            ("CreekLite 7'6\" 3 wt Pack Rod", "Four-piece ultralight rod built for tight back-country.", "Fly Rods", ["Beginner", "Freshwater", "Lightweight"]),
            ("Canyon Carbon 10' 4 wt Euro-Nymph", "Extra reach and ultralight tip for tight-line nymphing.", "Fly Rods", ["Expert", "Freshwater", "Nymph"]),
            ("GlacierGlass 8' 5 wt Fiberglass", "Retro glass feel—perfect for small dries and roll casts.", "Fly Rods", ["Intermediate", "Freshwater"]),
            ("DriftCast Large-Arbor Reel 5/6", "CNC-machined, sealed drag—zero startup inertia.", "Fly Reels", ["Intermediate", "Freshwater"]),
            ("SurfRunner Sealed Reel 8/9", "Full-seal drag keeps salt and sand out on big water.", "Fly Reels", ["Expert", "Saltwater"]),
            ("BrookClick Click-Pawl Reel 3/4", "Feather-light click-pawl reel for the purist.", "Fly Reels", ["Beginner", "Freshwater", "Lightweight"]),
            ("Precision WF-5-F Floating Line", "True-to-weight line with long head for delicate dries.", "Fly Lines", ["Beginner", "Freshwater", "Dry Fly"]),
            ("BlueWater WF-8-I Intermediate", "Slow-sink clear tip—great for bait-busting stripers.", "Fly Lines", ["Expert", "Saltwater", "Streamer"]),
            ("Stealth Euro-Nymph Comp Line", "Micro-diameter level line; ultra-sensitive strike feel.", "Fly Lines", ["Expert", "Freshwater", "Nymph"]),
            ("Hatchling Dry Fly Assortment (24)", "CDC duns, spinners, and emergers for all hatch stages.", "Flies", ["Beginner", "Freshwater", "Dry Fly"]),
            ("Tungsten Nymph Selection (20)", "Heavy nymphs to reach the bottom fast in fast currents.", "Flies", ["Intermediate", "Freshwater", "Nymph"]),
            ("BigWater Streamer Box (12)", "Articulated, weighted streamers that move big fish.", "Flies", ["Expert", "Saltwater", "Streamer"]),
            ("Hi-Vis Indicator Yarn Pack", "Buoyant, easy-to-see yarn for subtle takes.", "Accessories", ["Beginner", "Freshwater"]),
            ("Rapid-Sink 5' PolyLeader", "Adds instant sink-tip versatility to any floating line.", "Accessories", ["Intermediate", "Freshwater", "Nymph"]),
            ("Flex-Grip Hemostats", "Non-slip jaws and micro-serrations for precise hook removal.", "Accessories", ["Beginner", "Freshwater"]),
            ("Nano-Spool Tippet Holder", "Mag-rim spool keeper—swaps sizes one-handed.", "Accessories", ["Intermediate", "Freshwater"]),
            ("Quick-Release Net Magnet", "Strong rare-earth magnet keeps your net secure yet handy.", "Accessories", ["Intermediate", "Freshwater"]),
            ("RiverReady Fly Patch", "Amadou and foam combo dries and stores flies stream-side.", "Accessories", ["Beginner", "Freshwater", "Dry Fly"]),
        ]

        for name, desc, cat_name, tag_list in products_payload:
            product = Product.objects.create(
                name=name,
                description=desc,
                category=categories[cat_name],
            )
            product.tags.set([tags[t] for t in tag_list])

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Category.objects.count()} categories, "
            f"{Tag.objects.count()} tags, and "
            f"{Product.objects.count()} products."
        ))
