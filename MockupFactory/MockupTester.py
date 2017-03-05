import MockFactory


def run():
    mf = MockFactory.MockupGen(r"D:\Dev\Debug", "testMF")
    mf.logo_loader()
    mf.product_loader()
    mf.product_mask_loader()
    mf.run_factory()

if __name__ == "__main__":
    run()
