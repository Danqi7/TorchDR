from typing import Optional

from torchdr.affinity import NegativeCostAffinity, NegPotentialAffinity
from torchdr.affinity_matcher import AffinityMatcher


class PHATE(AffinityMatcher):
    r"""Implementation of PHATE introduced in :cite:`moon2019visualizing`.

    PHATE is a diffusion map-based method that uses a potential distance
    matrix to embed the data.

    Parameters
    ----------
    n_neighbors : int, optional
        Number of nearest neighbors. Default is 10.
    n_components : int, optional
        Dimension of the embedding space. Default is 2.
    t : int, optional
        Diffusion time parameter. Default is 5.
    eps : float, optional
        Small value to avoid division by zero in the affinity matrix.
        Default is 1e-5.
    backend : {"keops", None}, optional
        Which backend to use for handling sparsity and memory efficiency.
        Default is None.
    optimizer : str or torch.optim.Optimizer, optional
        Name of an optimizer from torch.optim or an optimizer class.
        Default is "Adam".
    optimizer_kwargs : dict, optional
        Additional keyword arguments for the optimizer.
    lr : float or 'auto', optional
        Learning rate for the optimizer. Default is 1e0.
    scheduler : str or torch.optim.lr_scheduler.LRScheduler, optional
        Name of a scheduler from torch.optim.lr_scheduler or a scheduler class.
        Default is None (no scheduler).
    scheduler_kwargs : dict, optional
        Additional keyword arguments for the scheduler.
    min_grad_norm : float, optional
        Tolerance for stopping criterion. Default is 1e-7.
    max_iter : int, optional
        Maximum number of iterations. Default is 1000.
    init : str, torch.Tensor, or np.ndarray, optional
        Initialization method for the embedding. Default is "pca".
    init_scaling : float, optional
        Scaling factor for the initial embedding. Default is 1e-4.
    device : str, optional
        Device to use for computations. Default is "auto".
    backend : {"keops", None}, optional
        Which backend to use for handling sparsity and memory efficiency.
        Default is None.
    verbose : bool, optional
        Verbosity of the optimization process. Default is False.
    random_state : float, optional
        Random seed for reproducibility. Default is None.
    check_interval : int, optional
        Number of iterations between two checks for convergence. Default is 50.
    """  # noqa: E501

    def __init__(
        self,
        n_neighbors: int = 10,
        n_components: int = 2,
        t: int = 5,
        eps: float = 1e-5,
        optimizer: str = "Adam",
        optimizer_kwargs: dict = {},
        lr: float = 1e0,
        scheduler: Optional[str] = None,
        scheduler_kwargs: dict = {},
        min_grad_norm: float = 1e-7,
        max_iter: int = 1000,
        init: str = "pca",
        init_scaling: float = 1.0,
        device: str = "auto",
        backend: Optional[str] = None,
        verbose: bool = False,
        random_state: Optional[float] = None,
        check_interval: int = 50,
    ):
        if backend == "faiss":
            raise ValueError(
                "[TorchDR] ERROR : FAISS backend is not supported for PHATE. "
                f"The {self.__class__.__name__} class does not support sparsity. "
                "Please use backend None or 'keops' instead."
            )

        self.n_neighbors = n_neighbors
        self.t = t
        self.eps = eps

        affinity_in = NegPotentialAffinity(
            backend=backend, device=device, eps=eps, t=t, K=n_neighbors
        )
        affinity_out = NegativeCostAffinity(backend=backend, device=device)
        loss_fn = "l2_loss"
        super().__init__(
            affinity_in=affinity_in,
            affinity_out=affinity_out,
            n_components=n_components,
            loss_fn=loss_fn,
            optimizer=optimizer,
            optimizer_kwargs=optimizer_kwargs,
            lr=lr,
            scheduler=scheduler,
            scheduler_kwargs=scheduler_kwargs,
            min_grad_norm=min_grad_norm,
            max_iter=max_iter,
            init=init,
            init_scaling=init_scaling,
            device=device,
            backend=backend,
            verbose=verbose,
            random_state=random_state,
            check_interval=check_interval,
        )
