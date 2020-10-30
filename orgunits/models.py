"""
Copyright 2020 ООО «Верме»
"""

from django.db import models
from django.db.models.expressions import RawSQL


class OrganizationQuerySet(models.QuerySet):
    def tree_downwards(self, root_org_id):
        """
        Возвращает корневую организацию с запрашиваемым root_org_id и всех её детей любого уровня вложенности
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python

        :type root_org_id: int
        """
        queryset = self
        for organization in queryset:
            if organization.id == root_org_id:
                continue
            elif organization.parent_id == root_org_id:
                continue
            elif organization.parent and organization.parent.parent_id == root_org_id:
                continue
            else:
                queryset = queryset.exclude(id=organization.id)
        return queryset

    def tree_upwards(self, child_org_id):
        """
        Возвращает корневую организацию с запрашиваемым child_org_id и всех её родителей любого уровня вложенности
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python
        :type child_org_id: int
        """
        queryset = self
        child_org = queryset.filter(id=child_org_id).first()
        print(child_org)
        for organization in queryset:
            if organization.id == child_org_id:
                continue
            elif organization.id == child_org.parent_id:
                continue
            elif child_org.parent and organization.id == child_org.parent.parent_id:
                continue
            else:
                queryset = queryset.exclude(id=organization.id)

        return queryset


class Organization(models.Model):
    """ Организаци """

    objects = OrganizationQuerySet.as_manager()

    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name="Название")
    code = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name="Код")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Вышестоящая организация",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Организация"
        verbose_name = "Организации"

    def parents(self):
        """
        Возвращает всех родителей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_upwards()
        :rtype: django.db.models.QuerySet
        """

        parents_without_self = Organization.objects.tree_upwards(self.id).exclude(id=self.id)
        return parents_without_self

    def children(self):
        """
        Возвращает всех детей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_downwards()
        :rtype: django.db.models.QuerySet
        """

        children_without_self = Organization.objects.tree_downwards(self.id).exclude(id=self.id)
        return children_without_self

    def __str__(self):
        return self.name