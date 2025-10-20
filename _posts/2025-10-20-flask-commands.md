---
title: "flask commands"
date: "2022-01-07T11:20:36+0100"
lastmod: "2022-01-07T11:20:36+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/linux-1.jpg"
description: "flask commands"

tags: ['flask', 'commands']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
with app.app_context():
    # needed to make CLI commands work
    @app.cli.command("reset")
    def reset_db():
        """Drops and Creates fresh database"""
        db.drop_all()
        db.create_all()

    @app.cli.command("boot")
    def bootstrap_db():
        """Drops and Creates fresh database"""
        db.drop_all()
        db.create_all()

        n1 = PortRangeNetworksModel(
            name="first",
            begin=100,
            end=200,
            description="One differnet This is my first desc.")
        n2 = PortRangeNetworksModel(
            name="second",
            begin=300,
            end=400,
            description="Two differnet This is my first desc.")
        n3 = PortRangeNetworksModel(
            name="third",
            begin=500,
            end=600,
            description="Three differnet This is my first desc.")
        n4 = PortRangeNetworksModel(
            name="fourth",
            begin=700,
            end=800,
            description="Four differnet This is my first desc.")
        n5 = PortRangeNetworksModel(
            name="fifth",
            begin=900,
            end=950,
            description="Fift differnet This is my first desc.")
        n6 = PortRangeNetworksModel(
            name="six",
            begin=30000,
            end=40000,
            description="Six differnet This is my first desc.")

        vlan1 = VlansModel(vlan_id=30,
                           name='192_168_002_000_V0026_VDS',
                           name_network='cb.dmz.art-srv-eXX.prod',
                           subnet='192.168.2.1',
                           mask=24,
                           description='Unkown')
        vlan2 = VlansModel(vlan_id=31,
                           name='022_000_222_000_V0026_VDS',
                           name_network='sk.dmz.art-srv-eXX.prod',
                           subnet='192.168.0.1',
                           mask=24,
                           description='Unkown')
        vlan3 = VlansModel(vlan_id=40,
                           name='033_000_222_000_V0026_VDS',
                           name_network='cb.dmz.art-srv-eXX.prod',
                           subnet='10.0.0.0',
                           mask=8,
                           description='Unkown')
        vlan4 = VlansModel(vlan_id=50,
                           name='044_000_222_000_V0026_VDS',
                           name_network='cb.dmz.art-srv-eXX.prod',
                           subnet='172.16.0.0',
                           mask=16,
                           description='Unkown')
        vlan5 = VlansModel(vlan_id=14,
                           name='055_000_222_000_V0026_VDS',
                           name_network='cb.dmz.art-srv-eXX.prod',
                           subnet='192.168.12.0',
                           mask=24,
                           description='Unkown')
        vlan6 = VlansModel(vlan_id=12,
                           name='066_000_222_000_V0026_VDS',
                           name_network='cb.dmz.art-srv-eXX.prod',
                           subnet='192.168.11.0',
                           mask=24,
                           description='Unkown')

        vlan1.port_ranges_networks.extend((n1, n2, n3))
        vlan2.port_ranges_networks.extend((n4, n1))
        vlan3.port_ranges_networks.extend((n1, n2))
        vlan4.port_ranges_networks.extend((n2, n4))
        vlan5.port_ranges_networks.extend((n1, n3))
        vlan6.port_ranges_networks.extend((n3, n2, n6))

        prd1 = PortRangeDescriptionsModel(
            name="misko",
            range=5,
            description="TOto je Misko",
            start_ports=[0, 5],
            middleware_base_rev_id="93bc9c3c-db70-4f29-ac84-9e28568b7a86")
        prd2 = PortRangeDescriptionsModel(
            name="albert",
            range=10,
            description="TOto je Albert",
            start_ports=[0],
            middleware_base_rev_id="d14197d1-0875-4ed6-a6a1-425b51355580")
        prd3 = PortRangeDescriptionsModel(
            name="daniil",
            range=5,
            description="TOto je Daniil",
            start_ports=[0, 5],
            middleware_base_rev_id="306429f2-a38a-496a-8413-a09a32d72942")
        prd4 = PortRangeDescriptionsModel(
            name="ferko",
            range=10,
            description="TOto je Ferko",
            start_ports=[5],
            middleware_base_rev_id="1d46e0dd-a8e7-45de-871c-56e1be0604e0")

        pra1 = PortRangeApplicationsModel(
            begin=30000,
            end=30004,
            description="first",
            app_rev_id="d3884918-aecc-4d5c-a746-68a97d082399",
        )

        pra1.port_range_descriptions_id = 1
        pra1.port_range_networks_id = 2
        pra1.vlan_id = 2

        pra2 = PortRangeApplicationsModel(
            begin=30012,
            end=30021,
            description="second",
            app_rev_id="3eb18303-55f1-4bf5-b1f6-2137773496e9",
        )

        pra2.port_range_descriptions_id = 3
        pra2.port_range_networks_id = 2
        pra2.vlan_id = 3

        pra3 = PortRangeApplicationsModel(
            begin=30028,
            end=30037,
            description="third",
            app_rev_id="97ba3bc4-269e-4545-b04e-2183becdfe01",
        )

        pra3.port_range_descriptions_id = 3
        pra3.port_range_networks_id = 2
        pra3.vlan_id = 4

        db.session.add(vlan1)
        db.session.add(vlan2)
        db.session.add(vlan3)
        db.session.add(vlan4)
        db.session.add(vlan5)
        db.session.add(vlan6)
        db.session.add(n5)
        db.session.add(prd1)
        db.session.add(prd2)
        db.session.add(prd3)
        db.session.add(prd4)
        db.session.add(pra1)
        db.session.add(pra2)
        db.session.add(pra3)

        db.session.commit()


if __name__ == "__main__":
    ma.init_app(app)

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

```
