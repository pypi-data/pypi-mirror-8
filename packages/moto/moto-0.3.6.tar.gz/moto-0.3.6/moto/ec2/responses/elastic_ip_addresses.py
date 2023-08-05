from __future__ import unicode_literals
from jinja2 import Template

from moto.core.responses import BaseResponse
from moto.ec2.models import ec2_backend
from moto.ec2.utils import sequence_from_querystring


class ElasticIPAddresses(BaseResponse):
    def allocate_address(self):
        if "Domain" in self.querystring:
            domain = self.querystring.get('Domain')[0]
        else:
            domain = "standard"
        address = ec2_backend.allocate_address(domain)
        template = Template(ALLOCATE_ADDRESS_RESPONSE)
        return template.render(address=address)

    def associate_address(self):
        if "InstanceId" in self.querystring:
            instance = ec2_backend.get_instance(self.querystring['InstanceId'][0])
        elif "NetworkInterfaceId" in self.querystring:
            raise NotImplementedError("Lookup by allocation id not implemented")
        else:
            ec2_backend.raise_error("MissingParameter", "Invalid request, expect InstanceId/NetworkId parameter.")

        reassociate = False
        if "AllowReassociation" in self.querystring:
            reassociate = self.querystring['AllowReassociation'][0] == "true"

        if "PublicIp" in self.querystring:
            eip = ec2_backend.associate_address(instance, address=self.querystring['PublicIp'][0], reassociate=reassociate)
        elif "AllocationId" in self.querystring:
            eip = ec2_backend.associate_address(instance, allocation_id=self.querystring['AllocationId'][0], reassociate=reassociate)
        else:
            ec2_backend.raise_error("MissingParameter", "Invalid request, expect PublicIp/AllocationId parameter.")

        template = Template(ASSOCIATE_ADDRESS_RESPONSE)
        return template.render(address=eip)

    def describe_addresses(self):
        template = Template(DESCRIBE_ADDRESS_RESPONSE)

        if "Filter.1.Name" in self.querystring:
            raise NotImplementedError("Filtering not supported in describe_address.")
        elif "PublicIp.1" in self.querystring:
            public_ips = sequence_from_querystring("PublicIp", self.querystring)
            addresses = ec2_backend.address_by_ip(public_ips)
        elif "AllocationId.1" in self.querystring:
            allocation_ids = sequence_from_querystring("AllocationId", self.querystring)
            addresses = ec2_backend.address_by_allocation(allocation_ids)
        else:
            addresses = ec2_backend.describe_addresses()
        return template.render(addresses=addresses)

    def disassociate_address(self):
        if "PublicIp" in self.querystring:
            disassociated = ec2_backend.disassociate_address(address=self.querystring['PublicIp'][0])
        elif "AssociationId" in self.querystring:
            disassociated = ec2_backend.disassociate_address(association_id=self.querystring['AssociationId'][0])
        else:
            ec2_backend.raise_error("MissingParameter", "Invalid request, expect PublicIp/AssociationId parameter.")

        return Template(DISASSOCIATE_ADDRESS_RESPONSE).render()

    def release_address(self):
        if "PublicIp" in self.querystring:
            released = ec2_backend.release_address(address=self.querystring['PublicIp'][0])
        elif "AllocationId" in self.querystring:
            released = ec2_backend.release_address(allocation_id=self.querystring['AllocationId'][0])
        else:
            ec2_backend.raise_error("MissingParameter", "Invalid request, expect PublicIp/AllocationId parameter.")

        return Template(RELEASE_ADDRESS_RESPONSE).render()


ALLOCATE_ADDRESS_RESPONSE = """<AllocateAddressResponse xmlns="http://ec2.amazonaws.com/doc/2013-07-15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <publicIp>{{ address.public_ip }}</publicIp>
  <domain>{{ address.domain }}</domain>
  {% if address.allocation_id %}
    <allocationId>{{ address.allocation_id }}</allocationId>
  {% endif %}
</AllocateAddressResponse>"""

ASSOCIATE_ADDRESS_RESPONSE = """<AssociateAddressResponse xmlns="http://ec2.amazonaws.com/doc/2013-07-15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <return>true</return>
  {% if address.association_id %}
    <associationId>{{ address.association_id }}</associationId>
  {% endif %}
</AssociateAddressResponse>"""

DESCRIBE_ADDRESS_RESPONSE = """<DescribeAddressesResponse xmlns="http://ec2.amazonaws.com/doc/2013-07-15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <addressesSet>
    {% for address in addresses %}
        <item>
          <publicIp>{{ address.public_ip }}</publicIp>
          <domain>{{ address.domain }}</domain>
          {% if address.instance %}
            <instanceId>{{ address.instance.id }}</instanceId>
          {% else %}
            <instanceId/>
          {% endif %}
          {% if address.allocation_id %}
            <allocationId>{{ address.allocation_id }}</allocationId>
          {% endif %}
          {% if address.association_id %}
            <associationId>{{ address.association_id }}</associationId>
          {% endif %}
        </item>
    {% endfor %}
  </addressesSet>
</DescribeAddressesResponse>"""

DISASSOCIATE_ADDRESS_RESPONSE = """<DisassociateAddressResponse xmlns="http://ec2.amazonaws.com/doc/2013-07-15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <return>true</return>
</DisassociateAddressResponse>"""

RELEASE_ADDRESS_RESPONSE = """<ReleaseAddressResponse xmlns="http://ec2.amazonaws.com/doc/2013-07-15/">
  <requestId>59dbff89-35bd-4eac-99ed-be587EXAMPLE</requestId>
  <return>true</return>
</ReleaseAddressResponse>"""
