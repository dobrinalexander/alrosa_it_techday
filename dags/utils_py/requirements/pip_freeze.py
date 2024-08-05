import pkg_resources

# Получаем список установленных пакетов
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

# Записываем имена пакетов и их версии в файл requirements.txt
with open("utils_py/requirements/requirements.txt", "w") as f:
    for package, version in installed_packages.items():
        if package == "psycopg2":
            f.write(f"psycopg2-binary\n")
        else:
            f.write(f"{package}\n")
        # f.write(f"{package}=={version}\n")
