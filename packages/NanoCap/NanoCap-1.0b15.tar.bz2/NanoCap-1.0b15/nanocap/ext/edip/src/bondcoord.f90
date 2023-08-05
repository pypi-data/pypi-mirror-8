
      subroutine bondcoord

      include "common.f90"

!+----------------------+
!| Zi= zi + zj + zpi(i) |
!+----------------------+
      do jj=1,num(i)
	j=near(i,jj)
        z(i)=z(i) + zz(j)

	do kk=1,num(j)
	if ((dr(j,kk).gt.zlow).and.(dr(j,kk).lt.zhigh)) then
	  fac=dzz(j,kk)
	  finiteforce2(jj,kk)=.true.

          do ind=1,3
            dzdxx(jj,kk,ind)=dzdxx(jj,kk,ind) + fac*dxdr(j,kk,ind)
          end do
	end if
	end do

      end do
      end
